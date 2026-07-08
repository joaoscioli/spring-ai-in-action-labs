# Reviewer Guide

This guide helps a technical reviewer understand the AI engineering signals
demonstrated by this repository.

## What To Review First

1. `README.md` for repository purpose.
2. `docs/ai-engineering-positioning.md` for portfolio framing.
3. `docs/ai-safety-checklist.md` for safety boundaries.
4. `docs/evaluation-runbook.md` for evaluation approach.
5. `board-game-buddy/` for the runnable Spring AI lab.

## Strong Signals

- AI features are treated as software features with contracts, tests, and
  failure modes.
- Prompt behavior, cost, latency, rollout, and evaluation are documented.
- The lab separates deterministic API behavior from model-assisted behavior.
- Tests protect input boundaries and provider integration assumptions.

## Interview Talking Points

- Explain why AI output needs evaluation rather than only unit tests.
- Discuss prompt injection, cost control, and safe rollout.
- Show how Spring AI fits into a normal backend engineering workflow.
