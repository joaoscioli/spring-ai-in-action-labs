# Spring AI Engineering Labs

> Portfolio status: active AI engineering lab for Java and Spring Boot.

This repository explores how modern AI capabilities can be built into backend
systems using Java, Spring Boot, and Spring AI.

The goal is not to present AI as a buzzword. The goal is to show practical AI
engineering: prompts, structured outputs, tool calling, retrieval, evaluation,
security, observability, and production trade-offs.

## Why This Repository Exists

AI is becoming part of everyday software products. For backend engineers, the
valuable skill is not only calling an LLM API. The valuable skill is designing
AI-assisted features that are reliable, testable, observable, and useful to the
business.

This lab focuses on:

- Spring AI fundamentals;
- LLM-backed backend features;
- prompt design and prompt boundaries;
- prompt versioning and input guardrails;
- structured responses;
- tool calling from application services;
- retrieval-augmented generation;
- evaluation and test strategy;
- cost, latency, and observability;
- stakeholder-friendly examples.

## Current Scope

The current implementation includes:

- `board-game-buddy`: an experimental Spring Boot and Spring AI application.

Current sections:

- [AI Engineering Positioning](docs/ai-engineering-positioning.md)
- [Reviewer Scorecard](docs/reviewer-scorecard.md)
- [Technical Depth Map](docs/technical-depth-map.md)
- [Portfolio Positioning](docs/portfolio-positioning.md)
- [Hiring Manager Summary](docs/hiring-manager-summary.md)
- [30-Second Pitch](docs/30-second-pitch.md)
- [Interview Route](docs/interview-route.md)
- [Interview Case Study](docs/interview-case-study.md)
- [Key Talking Points](docs/key-talking-points.md)
- [Pre-Interview Checklist](docs/pre-interview-checklist.md)
- [Tough Interview Questions](docs/tough-interview-questions.md)
- [Senior Review Notes](docs/senior-review-notes.md)
- [Architecture Review Checklist](docs/architecture-review-checklist.md)
- [Business Value](docs/business-value.md)
- [Technical Debt Register](docs/technical-debt-register.md)
- [Decision Log](docs/decision-log.md)
- [Next Review Focus](docs/next-review-focus.md)
- [Demo Script](docs/demo-script.md)
- [Interview Questions](docs/interview-questions.md)
- [Local Development](docs/local-development.md)
- [CI Workflow](docs/ci.md)
- [Repository Hygiene](docs/repository-hygiene.md)
- [Spring AI Fundamentals](docs/spring-ai-fundamentals.md)
- [Board Game Buddy API](docs/board-game-buddy-api.md)
- [Prompt and Response Patterns](docs/prompt-response-patterns.md)
- [Tool Calling](docs/tool-calling.md)
- [Retrieval-Augmented Generation](docs/rag-pattern.md)
- [Evaluation and Observability](docs/evaluation-observability.md)
- [Evaluation Dataset Template](docs/evaluation-dataset-template.md)
- [Evaluation Runbook](docs/evaluation-runbook.md)
- [AI Cost And Latency Strategy](docs/cost-latency-strategy.md)
- [Model Selection](docs/model-selection.md)
- [AI Feature Rollout](docs/ai-feature-rollout.md)
- [AI Safety Checklist](docs/ai-safety-checklist.md)
- [Implementation Examples](docs/implementation-examples.md)
- [Prompt Versioning](docs/prompt-versioning.md)
- [Stakeholder Demo Scenarios](docs/stakeholder-demo-scenarios.md)
- [Repository Roadmap](docs/roadmap.md)
- [Changelog](CHANGELOG.md)

Planned sections:

- runnable implementation examples.

## Portfolio Role

This is an emerging-technology repository in my backend portfolio.

It complements my production-minded Java and Spring Boot projects by showing
that I can evaluate new frameworks, connect them to business use cases, and
explain the engineering trade-offs behind AI features.

## Interview Checkpoint

A reviewer should inspect `board-game-buddy`, prompt versioning, input
guardrails, and WireMock tests first. These show AI features being treated as
backend features with contracts, safety boundaries, and evaluation thinking.

## Portfolio Proof

This repository proves emerging-technology judgment. It shows AI integration as
software engineering work: prompts, validation, cost, safety, tests, and
stakeholder value.

## Fast Review Path

1. Read the [30-Second Pitch](docs/30-second-pitch.md) to understand the repository signal.
2. Open the [Interview Case Study](docs/interview-case-study.md) to follow the AI engineering story.
3. Inspect `board-game-buddy`, prompt versioning, guardrails, and WireMock tests to validate reviewability.

## Tech Focus

- Java 21
- Spring Boot
- Spring AI
- OpenAI Spring AI starter
- Gradle
- JUnit
- WireMock
- LLM integration
- AI feature evaluation

## Repository Principles

- Keep examples practical.
- Explain business value before implementation detail.
- Treat AI behavior as something that needs tests and evaluation.
- Avoid leaking secrets or model credentials.
- Document trade-offs around cost, latency, reliability, and safety.
- Preserve learning history while improving presentation quality.

## Interview Talking Points

- How AI features fit into backend systems.
- Why prompt design is part of engineering design.
- How to test AI-assisted behavior.
- When to use RAG instead of sending large prompts.
- How observability changes when LLMs are part of the request path.
