# Interview Defense Notes

Use these notes when a reviewer challenges the project scope or design choices.

## Likely Challenge

"Is this just an AI wrapper around an API call?"

## Defense

The repository should defend AI features as backend engineering problems:
validation, fallback behavior, prompt versioning, evaluation, observability,
cost, latency, and safety boundaries matter more than a raw model call.

## Evidence To Show

- `docs/evaluation-observability.md`
- `docs/technical-risks.md`
- `docs/acceptance-criteria.md`

## Senior Signal

The decision treats model behavior as an unreliable dependency that needs
contracts, monitoring, and operational controls.
