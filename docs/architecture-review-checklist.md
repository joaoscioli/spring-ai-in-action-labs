# Architecture Review Checklist

Use this checklist to review the project as an AI-enabled backend exercise.

## AI Boundary

- Prompt construction, model calls, validation, and fallbacks are separated.
- Model output is treated as untrusted input until validated.
- Prompt versions are reviewable as behavior changes.

## Production Risk

- Sensitive data is excluded from prompts unless there is a clear reason.
- Cost, latency, and failure modes are visible in the design.
- Deterministic logic is tested without depending on live model responses.

## Evaluation

- Expected model behavior can be checked with repeatable examples.
- Safety constraints are documented before adding more features.
- Observability explains model usage, errors, and fallback decisions.

## Interview Defense

Be ready to explain how this project avoids being just a wrapper around an LLM
and instead shows engineering controls around AI behavior.
