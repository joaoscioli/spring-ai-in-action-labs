# Security Policy

This repository is a Spring AI engineering lab. Security review is especially
important because AI examples may involve prompts, API keys, tools, and model
outputs.

## Supported Scope

Security review focuses on:

- API keys or model credentials committed by mistake;
- prompt injection risks in examples;
- unsafe tool-calling behavior;
- sensitive data included in prompts, logs, or fixtures;
- dependency risk in the Spring Boot application.

## Reporting A Security Concern

Open a concise issue describing the affected example or document. Do not post
real API keys, customer data, private prompts, or exploitable details.

## Development Practices

- Keep model credentials out of Git.
- Use synthetic prompts and fixtures.
- Document safety boundaries for AI-assisted features.
