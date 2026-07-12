# Prompt Versioning

Prompts are part of AI feature behavior and should be versioned deliberately.

## Why Prompt Versioning Matters

A prompt change can affect:

- answer quality;
- response structure;
- safety behavior;
- latency;
- token cost;
- evaluation results.

Versioning helps teams understand which prompt produced which behavior.

## Suggested Metadata

Track:

- prompt name;
- prompt version;
- feature name;
- model name;
- release date;
- evaluation dataset version;
- known limitations.

## Change Process

Before changing a prompt:

1. Describe the reason for the change.
2. Run existing evaluation examples.
3. Compare answer quality and failure modes.
4. Record cost or latency changes.
5. Update the prompt version.

## Logging Direction

Logs should include prompt version, not necessarily full prompt content.

Avoid logging sensitive prompt data directly.

## Input Guardrails

Prompt versioning works best with request validation. Blank, missing, or
oversized user input should be rejected before a model call so cost and behavior
remain predictable.

## Interview Talking Points

- Prompt changes are behavior changes.
- Prompt versions help diagnose regressions.
- Evaluation should run when prompts change.
- Logging prompt version is safer than logging full prompt text.
- Input validation is part of AI reliability, not just API hygiene.
