# Security Policy

This repository explores AI features in backend systems, so security feedback
should focus on secrets, prompt data, model boundaries, dependencies, and
unsafe examples.

## Supported Scope

Security feedback is welcome for:

- accidental API key or model credential exposure;
- unsafe prompt or input-handling examples;
- dependency vulnerabilities;
- examples that send unnecessary sensitive data to a model;
- misleading safety, evaluation, or rollout guidance.

## Reporting

Please do not open a public issue with sensitive details.

Send a private report to `joaoscioli@outlook.com` with the affected file, the
risk, and a suggested mitigation when possible.

## Security Expectations

- Model credentials must never be committed.
- Prompts should avoid secrets and unnecessary personal data.
- AI behavior changes should include safety or evaluation notes when relevant.
