# Interview Case Study

Use this case study to explain the repository as an AI engineering discussion.

## Scenario

A backend product wants to add an AI-assisted feature without treating the model
as an unreviewable black box.

## Decision

Use Spring AI with a small `board-game-buddy` example and surround model-backed
behavior with prompt versioning, input guardrails, API contracts, WireMock
tests, evaluation notes, cost and latency thinking, and safety documentation.

## Evidence To Show

- `board-game-buddy/src/main/java/com/example/boardgamebuddy/SpringAiBoardGameService.java`
- `board-game-buddy/src/test/java/com/example/boardgamebuddy/SpringAiBoardGameServiceWireMockTests.java`
- `docs/prompt-versioning.md`
- `docs/evaluation-runbook.md`

## Trade-Off

The repository does not present AI as a shortcut around deterministic design.
It shows where model behavior can help, where validation should happen before
the model call, and where evaluation is needed after prompt changes.

## Strong Interview Close

"The engineering challenge is not calling an LLM. The challenge is making the
AI-assisted behavior testable, observable, safe, useful, and understandable to
stakeholders."
