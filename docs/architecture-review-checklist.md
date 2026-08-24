# Architecture Review Checklist

Use this checklist to review the project's AI-enabled backend architecture. Support each item with code, tests, configuration, or documentation.

## AI Boundary

- [ ] Prompt construction, model calls, output validation, and fallbacks have distinct responsibilities.
- [ ] Model output remains untrusted until it passes validation.
- [ ] Prompt changes are versioned and reviewable.

## Production Risk

- [ ] Prompts exclude sensitive data unless its use is documented and controlled.
- [ ] The design exposes model cost, latency, failures, and fallback behavior.
- [ ] Deterministic logic is tested without live model calls.

## Evaluation

- [ ] Repeatable examples verify expected model behavior.
- [ ] Safety constraints are explicit and testable.
- [ ] Logs and metrics explain model usage, errors, and fallback decisions.

## Architecture Defense

Be ready to explain the controls that make this more than an LLM wrapper, the evidence that they work, and the next production risk to address.
