
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
