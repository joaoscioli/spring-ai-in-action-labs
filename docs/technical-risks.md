# Technical Risks

This file captures the main risks in Spring AI features and how the project
plans to reduce them.

## Risks

- Model output can be invalid, unsafe, or inconsistent.
- Prompt changes can silently alter product behavior.
- Latency and token cost can grow without visibility.
- Sensitive data can be sent to model providers without clear controls.

## Mitigations

- Validate and normalize model output before using it.
- Version prompts and record evaluation examples.
- Track cost, latency, and fallback behavior.
- Define data-handling boundaries before adding real user data.

## Interview Angle

The strongest discussion is treating AI as an unreliable external dependency
that needs contracts, evaluation, monitoring, and safety controls.
