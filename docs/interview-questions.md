# Interview Questions

Use these questions to prepare an AI engineering discussion.

## What is the main engineering signal in this repository?

The main signal is treating AI behavior as backend behavior: prompts have
versions, inputs need guardrails, responses need contracts, and changes need
evaluation.

## Why are tests still useful with LLM features?

Tests can protect deterministic behavior around the model: validation,
request construction, fallback paths, API contracts, and integrations mocked
with predictable responses.

## What should not be sent to an LLM?

Secrets, unnecessary personal data, large unfiltered inputs, and business data
without a clear purpose should stay out of model prompts.

## What is the senior-level signal?

The senior signal is connecting AI features to product value while managing
cost, latency, safety, observability, and evaluation instead of only calling a
model API.
