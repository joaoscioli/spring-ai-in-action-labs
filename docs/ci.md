# CI Workflow

This repository uses GitHub Actions to run the `board-game-buddy` test suite on
pushes to `main` and on pull requests.

## What The Workflow Checks

- The Spring Boot and Spring AI application builds on a clean Linux runner.
- Java 17 is available, matching the Gradle toolchain configuration.
- The Gradle wrapper can run the automated test suite.
- AI-related tests stay executable without leaking real API credentials.

## Why This Matters

AI features need the same engineering discipline as other backend features:
repeatable tests, isolated configuration, and clear feedback when behavior
changes. The workflow gives reviewers a visible signal that the repository is
being treated as production-minded engineering work, not only experimentation.

## Future Improvements

- Add a separate evaluation job for prompt and response quality checks.
- Publish test reports as workflow artifacts on failure.
- Add dependency review and secret scanning gates.
