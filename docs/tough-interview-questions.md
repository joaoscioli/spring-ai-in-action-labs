# Tough Interview Questions

Use these questions to prepare direct, technical answers.

## Is this only a wrapper around an LLM?

No. The important engineering work is around the model call: validation, prompt
versioning, tests, evaluation, cost, latency, safety, and fallback behavior.

## What should not be sent to a model?

Secrets, unnecessary personal data, private business data without purpose, and
large unfiltered inputs should stay out of prompts.

## How can AI behavior be tested?

Deterministic boundaries can be tested: validation, request construction,
fallback behavior, API contracts, and mocked model responses.

## What would you defend in a code review?

Treating prompt changes as behavior changes that need review and evaluation.
