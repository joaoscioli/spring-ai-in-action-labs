import json
import unittest
import subprocess
import sys
import threading
from contextlib import redirect_stderr
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO, StringIO
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

from evaluate import evaluate, main, passes


class EvaluationTests(unittest.TestCase):
    @patch("evaluate.perf_counter", side_effect=[10.0, 10.125, 20.0, 20.25])
    @patch("evaluate.urlopen")
    def test_latency_is_recorded_for_success_and_transport_failure_without_answer_text(self, open_url, clock):
        open_url.side_effect = [BytesIO(b'{"answer":"Diagonally."}'), URLError("private diagnostic")]
        case = {"id": "first", "question": "How does a bishop move?", "required_patterns": ["Diagonal"]}
        results = evaluate("http://localhost:8080", [case, dict(case, id="second")], 2)
        self.assertEqual([125.0, 250.0], [item["latency_ms"] for item in results])
        self.assertEqual(["matched", "request_failed"], [item["reason"] for item in results])
        self.assertNotIn("Diagonally", json.dumps(results))
        self.assertNotIn("private diagnostic", json.dumps(results))
        self.assertEqual(4, clock.call_count)

    @patch("evaluate.urlopen")
    def test_forbidden_pattern_fails_even_when_all_required_patterns_match(self, open_url):
        case = {"id": "bishop", "question": "How does a bishop move?",
                "required_patterns": ["(?i)diagonal"],
                "forbidden_patterns": ["(?i)horizontally", "(?i)vertically"]}
        for answer, expected in (("Diagonally.", True),
                                 ("Diagonally and horizontally.", False),
                                 ("Diagonally or VERTICALLY.", False),
                                 ("Horizontally.", False)):
            with self.subTest(answer=answer):
                open_url.return_value = BytesIO(json.dumps({"answer": answer}).encode())
                result = evaluate("http://localhost:8080", [case], 2)[0]
                self.assertEqual(expected, result["passed"])
                self.assertEqual("matched" if expected else "rubric_mismatch", result["reason"])
                self.assertNotIn(answer, json.dumps(result))

    @patch("evaluate.urlopen")
    def test_invalid_forbidden_patterns_in_later_case_prevent_all_requests(self, open_url):
        valid = {"id": "first", "question": "How does a bishop move?",
                 "required_patterns": ["diagonal"]}
        for forbidden in (None, "horizontal", [None], [""], [" "], ["["]):
            with self.subTest(forbidden=forbidden):
                with self.assertRaises(ValueError):
                    evaluate("http://localhost:8080",
                             [valid, dict(valid, id="second", forbidden_patterns=forbidden)], 2)
        open_url.assert_not_called()

    def test_optional_empty_forbidden_patterns_preserve_existing_rubrics(self):
        case = {"required_patterns": ["diagonal"]}
        self.assertTrue(passes(case, "diagonal"))
        self.assertTrue(passes(dict(case, forbidden_patterns=[]), "diagonal"))

    @patch("evaluate.urlopen")
    def test_cli_reports_invalid_dataset_as_usage_error_without_requests(self, open_url):
        errors = StringIO()
        with patch.object(sys, "argv", ["evaluate.py"]), \
                patch("evaluate.Path.read_text", return_value="[]"), redirect_stderr(errors):
            with self.assertRaises(SystemExit) as failure:
                main()
        self.assertEqual(2, failure.exception.code)
        self.assertIn("cases must be a nonempty list", errors.getvalue())
        open_url.assert_not_called()

    @patch("evaluate.urlopen")
    def test_invalid_datasets_fail_before_any_request_including_a_later_bad_case(self, open_url):
        valid = {"id": "valid", "question": "How does a bishop move?",
                 "required_patterns": ["diagonal"]}
        invalid_cases = [None, [], {}, [None]]
        for field, values in {
            "id": [None, "", " "],
            "question": [None, "", " ", "x" * 501],
            "required_patterns": [None, [], "diagonal", [None], [""], [" "], ["["]],
        }.items():
            for value in values:
                invalid = dict(valid, id="second")
                invalid[field] = value
                invalid_cases.append([valid, invalid])
        invalid_cases.append([valid, dict(valid)])
        for cases in invalid_cases:
            with self.subTest(cases=cases):
                with self.assertRaises(ValueError):
                    evaluate("http://localhost:8080", cases, 2)
        open_url.assert_not_called()

    @patch("evaluate.urlopen")
    def test_valid_question_boundary_and_multiple_patterns_are_evaluated(self, open_url):
        cases = [{"id": "boundary", "question": "x" * 500,
                  "required_patterns": ["(?i)diagonal", "board"]}]
        open_url.return_value = BytesIO(b'{"answer":"Diagonally across the board."}')
        results = evaluate("http://localhost:8080", cases, 2)
        self.assertEqual({"id": "boundary", "passed": True, "reason": "matched"},
                         {key: value for key, value in results[0].items() if key != "latency_ms"})
        self.assertGreaterEqual(results[0]["latency_ms"], 0)
        self.assertEqual(1, open_url.call_count)

    @patch("evaluate.urlopen")
    def test_invalid_timeouts_fail_before_any_http_request(self, open_url):
        for timeout in (0, -1, float("nan"), float("inf"), float("-inf")):
            with self.subTest(timeout=timeout):
                with self.assertRaisesRegex(ValueError, "finite and greater than zero"):
                    evaluate("http://localhost:8080", [{"id": "unused"}], timeout)
        open_url.assert_not_called()

    def test_cli_rejects_nonfinite_and_nonpositive_timeouts_as_usage_errors(self):
        for timeout in ("0", "-1", "nan", "inf", "-inf"):
            with self.subTest(timeout=timeout):
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("evaluate.py")),
                     "--timeout=" + timeout], capture_output=True, text=True, timeout=10)
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn("finite and greater than zero", result.stderr)
                self.assertEqual("", result.stdout)

    def setUp(self):
        self.cases = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))

    def test_reference_answers_pass_and_fallbacks_or_wrong_answers_fail(self):
        for case, good, wrong in zip(self.cases, (
            "The base game supports three to four players.",
            "A bishop moves diagonally across the board.",
            "I can only help with board games.",
        ), ("Two players.", "Horizontally.", "Boil pasta in water.")):
            with self.subTest(case=case["id"]):
                self.assertTrue(passes(case, good))
                for bad in (wrong, "The board game assistant is unavailable right now.", "", None):
                    self.assertFalse(passes(case, bad))

    @patch("evaluate.urlopen")
    def test_posts_each_question_once_and_continues_after_transport_failure(self, open_url):
        open_url.side_effect = [
            BytesIO(b'{"answer":"Three to four players."}'),
            URLError("private diagnostic"),
            BytesIO(b'{"answer":"I can only help with board games."}'),
        ]
        results = evaluate("http://localhost:8080/", self.cases, 2)
        self.assertEqual([True, False, True], [item["passed"] for item in results])
        self.assertEqual("request_failed", results[1]["reason"])
        self.assertNotIn("private diagnostic", json.dumps(results))
        self.assertEqual(3, open_url.call_count)
        for call, case in zip(open_url.call_args_list, self.cases):
            request = call.args[0]
            self.assertEqual("http://localhost:8080/ask", request.full_url)
            self.assertEqual("POST", request.method)
            self.assertEqual({"question": case["question"]}, json.loads(request.data))
            self.assertEqual(2, call.kwargs["timeout"])

    @patch("evaluate.urlopen")
    def test_malformed_or_missing_answers_fail_without_false_success(self, open_url):
        for response in (b'not json', b'{}', b'[]', b'{"answer":42}'):
            with self.subTest(response=response):
                open_url.return_value = BytesIO(response)
                self.assertFalse(evaluate("http://localhost:8080", self.cases[:1], 2)[0]["passed"])

    def test_command_exit_code_matches_results_over_real_local_http(self):
        answers = dict(zip((case["question"] for case in self.cases), (
            "Three to four players.", "Diagonally.", "I can only help with board games."
        )))
        requests = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(self.path)
                question = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                body = json.dumps({"answer": answers[question["question"]]}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            command = [sys.executable, str(Path(__file__).with_name("evaluate.py")),
                       "--base-url", "http://127.0.0.1:" + str(server.server_port), "--timeout", "2"]
            good = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(0, good.returncode, good.stderr)
            self.assertEqual(3, json.loads(good.stdout)["passed"])

            answers[self.cases[0]["question"]] = "I couldn't generate an answer. Please try again."
            bad = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(1, bad.returncode, bad.stderr)
            self.assertEqual(2, json.loads(bad.stdout)["passed"])
            self.assertEqual(["/ask"] * 6, requests)
        finally:
            server.shutdown()
            worker.join(timeout=2)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
