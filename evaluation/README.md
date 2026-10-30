
Response bodies are limited to 1 MiB before JSON parsing. Oversized responses
fail that case as `request_failed`; later cases still run, and response content
is excluded from the report. This bounds response buffering, not total process memory.

Use `python evaluation/evaluate.py --cases path/to/dataset.json` to evaluate a custom
dataset without editing the bundled cases. Relative paths resolve from the current
directory. The default remains the bundled `cases.json` next to the script. Missing
files, malformed JSON, and invalid cases exit with code 2 before any API request.

Use `--repeat 3` to run three sequential passes over the same dataset and expose
answer variability. Repeated results include a one-based `attempt`; latency and
passed counts include every attempt, and any failure makes the command exit 1.
The default is one pass. Each repetition sends new API requests and may incur
provider charges; this is sampling, not an automatic retry policy.

The JSON report also includes `case_summary`: one entry per dataset ID in dataset
order, with attempt count, passed count, pass rate (0–1), and latency statistics
including failed attempts. Use this to spot an unstable question hidden by the
overall passed count. The detailed `cases` and strict any-failure exit code remain
available; a high sampled pass rate does not guarantee future model behavior.

The report's `failure_counts` separates `request_failed`, `rubric_mismatch` and
`latency_exceeded`, including zero counts. Each failed attempt contributes once:
an answer that misses the rubric remains a quality failure even when slow.
Use these counts to distinguish availability, answer quality and response-time
problems without including provider diagnostics or answer text in the report.
