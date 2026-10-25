import json
import unittest
import subprocess
import sys
import threading
from contextlib import redirect_stderr, redirect_stdout
from http.client import IncompleteRead
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO, StringIO
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from evaluate import MAX_RESPONSE_BYTES, evaluate, main, passes, summarize_latency


class EvaluationTests(unittest.TestCase):
    @patch("evaluate.urlopen")
    def test_response_size_boundary_is_bounded_closed_and_does_not_stop_later_cases(self, open_url):
        case = {"id": "boundary", "question": "How does a bishop move?",
                "required_patterns": ["Diagonal"]}
        prefix = b'{"answer":"Diagonally.","padding":"'
        suffix = b'"}'
        boundary = prefix + b'x' * (MAX_RESPONSE_BYTES - len(prefix) - len(suffix)) + suffix
        class BoundedResponse(BytesIO):
            def read(self, size=-1):
                if size != MAX_RESPONSE_BYTES + 1:
                    raise AssertionError("response must use a bounded read")
                return super().read(size)
        streams = [BoundedResponse(boundary), BoundedResponse(boundary + b' '),
                   BoundedResponse(b'{"answer":"Diagonally."}')]
        open_url.side_effect = streams

        results = evaluate("http://localhost:8080", [case, dict(case, id="oversized"),
                                                   dict(case, id="healthy")], 2)

        self.assertEqual(["matched", "request_failed", "matched"], [r["reason"] for r in results])
        self.assertTrue(all(stream.closed for stream in streams))
        self.assertEqual(3, open_url.call_count)
        self.assertNotIn("padding", json.dumps(results))

    @patch("evaluate.perf_counter", side_effect=[0, .125, 1, 1.25])
    @patch("evaluate.urlopen")
    def test_http_error_closes_response_without_reading_diagnostics_and_continues(self, open_url, clock):
        class PrivateResponse(BytesIO):
            def read(self, *args):
                self.fail_if_read = True
                raise AssertionError("error response body must not be read")

        body = PrivateResponse(b"private provider diagnostics")
        failure = HTTPError("http://localhost:8080/ask", 429, "private status", {}, body)
        healthy = BytesIO(b'{"answer":"Diagonally."}')
        open_url.side_effect = [failure, healthy]
        case = {"id": "limited", "question": "How does a bishop move?",
                "required_patterns": ["Diagonal"]}

        results = evaluate("http://localhost:8080", [case, dict(case, id="healthy")], 2)

        self.assertTrue(body.closed)
        self.assertTrue(healthy.closed)
        self.assertFalse(hasattr(body, "fail_if_read"))
        self.assertEqual(["request_failed", "matched"], [item["reason"] for item in results])
        self.assertEqual([False, True], [item["passed"] for item in results])
        self.assertEqual([125, 250], [item["latency_ms"] for item in results])
        self.assertNotIn("private", json.dumps(results))
        self.assertEqual(2, open_url.call_count)

    @patch("evaluate.perf_counter", side_effect=[0, .125, 1, 1.25])
    @patch("evaluate.urlopen")
    def test_truncated_http_response_is_reported_and_later_cases_still_run(self, open_url, clock):
        case = {"id": "truncated", "question": "How does a bishop move?",
                "required_patterns": ["Diagonal"]}
        class TruncatedResponse(BytesIO):
            def read(self, *args):
                raise IncompleteRead(b"private partial provider response", 100)
        open_url.side_effect = [TruncatedResponse(), BytesIO(b'{"answer":"Diagonally."}')]

        results = evaluate("http://localhost:8080", [case, dict(case, id="healthy")], 2)

        self.assertEqual([{"id": "truncated", "passed": False, "reason": "request_failed", "latency_ms": 125},
                          {"id": "healthy", "passed": True, "reason": "matched", "latency_ms": 250}], results)
        self.assertEqual(2, open_url.call_count)
        self.assertEqual(4, clock.call_count)
        self.assertNotIn("private", json.dumps(results))

    @patch("evaluate.urlopen")
    def test_optional_latency_budget_requires_correct_and_timely_answers(self, open_url):
        case = {"id": "bishop", "question": "How does a bishop move?",
                "required_patterns": ["Diagonal"], "max_latency_ms": 125}
        for answer, elapsed, reason in (("Diagonally.", .125, "matched"),
                                        ("Diagonally.", .1250001, "latency_exceeded"),
                                        ("Diagonally.", .25, "latency_exceeded"),
                                        ("Horizontally.", .25, "rubric_mismatch")):
            with self.subTest(answer=answer, elapsed=elapsed):
                open_url.return_value = BytesIO(json.dumps({"answer": answer}).encode())
                with patch("evaluate.perf_counter", side_effect=[0, elapsed]):
                    result = evaluate("http://localhost:8080", [case], 2)[0]
                self.assertEqual(reason, result["reason"])
                self.assertEqual(reason == "matched", result["passed"])
                self.assertEqual(round(elapsed * 1000, 3), result["latency_ms"])
                self.assertNotIn(answer, json.dumps(result))
        open_url.side_effect = URLError("private diagnostic")
        with patch("evaluate.perf_counter", side_effect=[0, .25]):
            self.assertEqual("request_failed", evaluate("http://localhost:8080", [case], 2)[0]["reason"])

    @patch("evaluate.urlopen")
    def test_cli_returns_failure_for_correct_answer_over_latency_budget(self, open_url):
        case = {"id": "bishop", "question": "How does a bishop move?",
                "required_patterns": ["Diagonal"], "max_latency_ms": 125}
        output = StringIO()
        open_url.return_value = BytesIO(b'{"answer":"Diagonally."}')
        with patch.object(sys, "argv", ["evaluate.py"]), \
                patch("evaluate.Path.read_text", return_value=json.dumps([case])), \
                patch("evaluate.perf_counter", side_effect=[0, .25]), \
                redirect_stdout(output):
            self.assertEqual(1, main())
        report = json.loads(output.getvalue())
        self.assertEqual(0, report["passed"])
        self.assertEqual("latency_exceeded", report["cases"][0]["reason"])
        self.assertEqual(250, report["latency"]["max_ms"])
        open_url.assert_called_once()

    @patch("evaluate.urlopen")
    def test_invalid_latency_budget_in_later_case_prevents_all_requests(self, open_url):
        valid = {"id": "first", "question": "How does a bishop move?", "required_patterns": ["diagonal"]}
        for limit in (None, True, False, "125", 0, -1, float("nan"), float("inf")):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "max_latency_ms"):
                evaluate("http://localhost:8080", [valid, dict(valid, id="second", max_latency_ms=limit)], 2)
        open_url.assert_not_called()

    def test_latency_summary_includes_failures_and_uses_nearest_rank_without_mutation(self):
        results = [{"latency_ms": value, "passed": value != 20} for value in range(20, 0, -1)]
        before = json.dumps(results)
        self.assertEqual({"count": 20, "mean_ms": 10.5, "p95_ms": 19, "max_ms": 20},
                         summarize_latency(results))
        self.assertEqual(before, json.dumps(results))
        self.assertEqual({"count": 1, "mean_ms": 0.125, "p95_ms": 0.125, "max_ms": 0.125},
                         summarize_latency([{"latency_ms": 0.125}]))
        self.assertEqual({"count": 0, "mean_ms": None, "p95_ms": None, "max_ms": None},
                         summarize_latency([]))

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
            self.assertEqual(summarize_latency(json.loads(good.stdout)["cases"]),
                             json.loads(good.stdout)["latency"])

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
