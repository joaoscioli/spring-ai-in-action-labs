# Next Review Focus

This file defines the next focused improvement for a technical reviewer to watch.

## Current Focus

Add a small evaluation dataset fixture for prompt version comparison.

## Why It Matters

The repository already has prompt versioning, guardrails, and WireMock tests. An
evaluation fixture would show how prompt changes are reviewed against expected
useful answers and expected refusals.

## Expected Evidence

- A small dataset with representative user prompts.
- Expected response categories such as useful answer, clarification, or refusal.
- A repeatable command or test that compares prompt versions.
