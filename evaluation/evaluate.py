"""Opt-in heuristic evaluation of a running /ask API; uses only the standard library."""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def passes(case, answer):
    return isinstance(answer, str) and all(
        re.search(pattern, answer) for pattern in case["required_patterns"]
    )


def evaluate(base_url, cases, timeout):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be finite and greater than zero")
    results = []
    for case in cases:
        request = Request(
            base_url.rstrip("/") + "/ask",
            data=json.dumps({"question": case["question"]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                answer = json.load(response).get("answer")
            passed = passes(case, answer)
            result = {"id": case["id"], "passed": passed,
                      "reason": "matched" if passed else "rubric_mismatch"}
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, AttributeError):
            # Keep provider diagnostics and answer text out of the evaluation report.
            result = {"id": case["id"], "passed": False, "reason": "request_failed"}
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and greater than zero")
    cases = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))
    results = evaluate(args.base_url, cases, args.timeout)
    print(json.dumps({"cases": results, "passed": sum(item["passed"] for item in results)}, indent=2))
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
