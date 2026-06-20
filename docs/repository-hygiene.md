# Repository Hygiene

This document defines the cleanup direction for the Spring AI lab.

## Current Situation

The `board-game-buddy` project has generated Gradle build artifacts tracked in
the repository history.

Examples include:

- compiled `.class` files;
- Gradle test reports;
- Gradle test result binaries;
- generated resources under `build/`.

## Why This Matters

Generated build artifacts make reviews noisier because local test runs can
modify tracked files. That creates distracting diffs unrelated to source code,
tests, or documentation.

## Recommended Cleanup

The best next step is to remove tracked generated files from the repository
while preserving history.

This means:

- keep the commits that already exist;
- delete generated `build/` files from the current branch;
- keep `.gitignore` rules so new generated files stay untracked;
- commit the cleanup separately with a clear message.

## Impact

This does not erase past commits. It only removes generated artifacts from the
current repository state so future changes are easier to review.

## Portfolio Signal

A clean repository tells reviewers that source code, tests, and documentation
are the intentional deliverables. Build outputs should be reproducible, not
stored as portfolio content.
