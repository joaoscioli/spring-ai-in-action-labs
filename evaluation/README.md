
Response bodies are limited to 1 MiB before JSON parsing. Oversized responses
fail that case as `request_failed`; later cases still run, and response content
is excluded from the report. This bounds response buffering, not total process memory.
