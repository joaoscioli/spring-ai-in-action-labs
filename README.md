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
- [Spring AI Fundamentals](docs/spring-ai-fundamentals.md)
- [Prompt and Response Patterns](docs/prompt-response-patterns.md)
- [Tool Calling](docs/tool-calling.md)
- [Retrieval-Augmented Generation](docs/rag-pattern.md)
- [Evaluation and Observability](docs/evaluation-observability.md)
- [Evaluation Dataset Template](docs/evaluation-dataset-template.md)
- [AI Cost And Latency Strategy](docs/cost-latency-strategy.md)
- [AI Safety Checklist](docs/ai-safety-checklist.md)
- [Implementation Examples](docs/implementation-examples.md)
- [Prompt Versioning](docs/prompt-versioning.md)
- [Stakeholder Demo Scenarios](docs/stakeholder-demo-scenarios.md)
- [Repository Roadmap](docs/roadmap.md)

Planned sections:

- runnable implementation examples.

## Portfolio Role

This is an emerging-technology repository in my backend portfolio.

It complements my production-minded Java and Spring Boot projects by showing
that I can evaluate new frameworks, connect them to business use cases, and
explain the engineering trade-offs behind AI features.

## Tech Focus

- Java 21
- Spring Boot
- Spring AI
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
