# Implementation Priority

This file defines the next implementation order for turning the repository into
a stronger Spring AI portfolio.

## P1: One Controlled AI Endpoint

- Add one Spring Boot endpoint that calls a model.
- Validate user input before the model call.
- Normalize and validate the model response.
- Provide a fallback path.

## P2: Evaluation And Observability

- Add prompt examples and expected output checks.
- Record latency, cost, and fallback considerations.
- Document what would be monitored in production.

## P3: Responsible AI Boundaries

- Add safety checks for sensitive data.
- Version prompts and document behavior changes.
- Define when the feature should fail closed.

## Why This Order

The repository should prove AI engineering discipline before adding larger RAG
or agent workflows. Controlled behavior beats impressive but unverified demos.
