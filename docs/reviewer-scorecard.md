# Reviewer Scorecard

Use this scorecard to review the repository quickly during portfolio screening.

## Strong Signals

- AI features are framed as backend engineering work, not model demos.
- Prompt versioning, input guardrails, evaluation, cost, and latency are documented.
- WireMock tests keep model integration behavior reviewable.
- The repository explains stakeholder value and safety boundaries together.

## Evidence

- `board-game-buddy/src/main/java/com/example/boardgamebuddy/SpringAiBoardGameService.java`
- `board-game-buddy/src/test/java/com/example/boardgamebuddy/SpringAiBoardGameServiceWireMockTests.java`
- `docs/evaluation-runbook.md`
- `docs/ai-safety-checklist.md`

## Next Senior Step

Add a small evaluation dataset fixture and a repeatable command for comparing
prompt versions against expected refusals and useful answers.
