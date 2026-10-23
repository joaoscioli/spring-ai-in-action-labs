"""Opt-in heuristic evaluation of a running /ask API; uses only the standard library."""

import argparse
import json
import math
import re
import sys
from http.client import HTTPException
from time import perf_counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def passes(case, answer):
    return isinstance(answer, str) and all(
        re.search(pattern, answer) for pattern in case["required_patterns"]
    ) and not any(re.search(pattern, answer) for pattern in case.get("forbidden_patterns", []))


def validate_cases(cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    seen = set()
    for index, case in enumerate(cases):
        prefix = f"case {index + 1}: "
        if not isinstance(case, dict):
            raise ValueError(prefix + "must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            raise ValueError(prefix + "id must be a unique nonblank string")
        seen.add(case_id)
        limit = case.get("max_latency_ms")
        if "max_latency_ms" in case and (isinstance(limit, bool) or not isinstance(limit, (int, float))
                                         or not math.isfinite(limit) or limit <= 0):
            raise ValueError(prefix + "max_latency_ms must be finite and greater than zero")
        question = case.get("question")
        if not isinstance(question, str) or not question.strip() or len(question) > 500:
            raise ValueError(prefix + "question must contain 1-500 characters and not be blank")
        patterns = case.get("required_patterns")
        if not isinstance(patterns, list) or not patterns:
            raise ValueError(prefix + "required_patterns must be a nonempty list")
        forbidden = case.get("forbidden_patterns", [])
        if not isinstance(forbidden, list):
            raise ValueError(prefix + "forbidden_patterns must be a list")
        for pattern in patterns + forbidden:
            if not isinstance(pattern, str) or not pattern.strip():
                raise ValueError(prefix + "patterns must be nonblank strings")
            try:
                re.compile(pattern)
            except re.error:
                raise ValueError(prefix + "pattern must be a valid regular expression") from None


def evaluate(base_url, cases, timeout):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be finite and greater than zero")
    # Validate the entire dataset before the first potentially billable request.
    validate_cases(cases)
    results = []
    for case in cases:
        request = Request(
            base_url.rstrip("/") + "/ask",
            data=json.dumps({"question": case["question"]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = perf_counter()
        try:
            with urlopen(request, timeout=timeout) as response:
                answer = json.load(response).get("answer")
            passed = passes(case, answer)
            result = {"id": case["id"], "passed": passed,
                      "reason": "matched" if passed else "rubric_mismatch"}
        except (HTTPError, URLError, HTTPException, TimeoutError, OSError, ValueError, AttributeError):
            # Keep provider diagnostics and answer text out of the evaluation report.
            result = {"id": case["id"], "passed": False, "reason": "request_failed"}
        elapsed_ms = (perf_counter() - started) * 1000
        result["latency_ms"] = round(elapsed_ms, 3)
        if result["passed"] and elapsed_ms > case.get("max_latency_ms", math.inf):
            result.update(passed=False, reason="latency_exceeded")
        results.append(result)
    return results


def summarize_latency(results):
    """Aggregate all cases, including failures; p95 uses the nearest-rank rule."""
    values = sorted(item["latency_ms"] for item in results)
    if not values:
        return {"count": 0, "mean_ms": None, "p95_ms": None, "max_ms": None}
    return {"count": len(values), "mean_ms": round(sum(values) / len(values), 3),
            "p95_ms": values[math.ceil(0.95 * len(values)) - 1], "max_ms": values[-1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and greater than zero")
    try:
        cases = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))
        results = evaluate(args.base_url, cases, args.timeout)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({"cases": results, "passed": sum(item["passed"] for item in results),
                      "latency": summarize_latency(results)}, indent=2))
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
