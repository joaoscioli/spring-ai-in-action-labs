# Demo Script

Use this short script to present the repository in a technical interview.

## 3-Minute Walkthrough

1. Start with the goal: AI features treated as backend engineering work.
2. Show `board-game-buddy`, prompt versioning, input guardrails, and WireMock
   tests.
3. Explain how deterministic validation surrounds non-deterministic model
   behavior.
4. Close with the next step: a small evaluation dataset with expected refusals.

## What To Emphasize

- Prompt changes are behavior changes.
- AI features need validation, safety, evaluation, and observability.
- Stakeholder demos should include fallback behavior.

## Before The Interview

- Open the prompt versioning and input guardrail examples.
- Be ready to explain what should not be sent to an LLM.
- Prepare one example of evaluating a prompt change.

## Evidence To Open

- `board-game-buddy/src/main/java/com/example/boardgamebuddy/AskController.java`
- `board-game-buddy/src/main/java/com/example/boardgamebuddy/SpringAiBoardGameService.java`
- `board-game-buddy/src/test/java/com/example/boardgamebuddy/AskControllerTests.java`
- `board-game-buddy/src/test/java/com/example/boardgamebuddy/SpringAiBoardGameServiceWireMockTests.java`

## Avoid Saying

- "The AI answers the question." Instead, explain validation, evaluation, and
  fallback behavior.
- "Prompt engineering solves it." Instead, explain the surrounding backend
  controls.
