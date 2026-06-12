# Evaluation and Observability

AI-assisted features need evaluation and observability because model behavior
can change even when application code still compiles.

Traditional tests prove deterministic application behavior. Evaluation checks
whether model-assisted answers are useful, grounded, safe, and consistent enough
for the business workflow.

## Why Evaluation Matters

AI features can fail in ways normal services usually do not.

Examples:

- the answer is fluent but wrong;
- the answer ignores provided context;
- the answer invents unsupported facts;
- the answer leaks sensitive information;
- the answer format changes unexpectedly;
- latency or cost becomes too high.

Evaluation makes these risks visible.

## Evaluation Dataset

Start with a small dataset of realistic examples.

For a billing assistant, include questions such as:

- explain an active monthly subscription;
- explain a canceled annual subscription;
- explain a failed payment;
- answer when context is missing;
- refuse to invent refund policy details;
- identify when escalation is needed.

Each example should include:

- user question;
- input context;
- expected answer characteristics;
- expected sources when RAG is used;
- failure criteria.

## Evaluation Criteria

Useful criteria:

- groundedness: answer uses only provided context;
- correctness: answer matches business rules;
- completeness: answer includes required information;
- safety: answer avoids secrets and unsupported actions;
- structure: response matches expected schema;
- tone: answer is appropriate for the user or agent;
- latency: response time is acceptable;
- cost: token usage stays within expected limits.

## Unit Tests vs Evaluation

Use unit tests for deterministic code:

- prompt template rendering;
- DTO validation;
- fallback handling;
- service boundaries;
- tool input validation;
- authorization checks.

Use evaluation for model behavior:

- answer quality;
- hallucination rate;
- source usage;
- response usefulness;
- prompt regressions.

Both are necessary.

## Observability Signals

AI features should expose signals that help diagnose behavior.

Useful metrics:

- request count;
- model latency;
- provider error count;
- token usage;
- estimated cost;
- tool call count;
- retrieval result count;
- fallback count;
- parse failure count.

Useful logs:

- correlation id;
- feature name;
- model name;
- prompt version;
- retrieval document ids;
- tool names called;
- failure type;
- latency bucket.

## What Not To Log

Avoid logging:

- API keys;
- access tokens;
- passwords;
- raw prompts with sensitive customer data;
- full model responses containing private information;
- payment details;
- private documents retrieved for RAG.

Prefer logging references:

- prompt template version;
- source document id;
- chunk id;
- request id;
- user id hash when appropriate.

## Cost Controls

AI features should include cost awareness.

Useful controls:

- limit prompt size;
- limit retrieved chunks;
- cache safe repeated answers when possible;
- choose smaller models for simple tasks;
- track token usage by feature;
- separate experimental features from production paths;
- define budget alerts.

## Latency Controls

Useful controls:

- timeout model calls;
- provide fallback responses;
- avoid unnecessary tool calls;
- retrieve only relevant context;
- keep prompts concise;
- move long-running workflows to async processing when appropriate.

## Stakeholder Explanation

```text
We evaluate AI features because a successful API call does not guarantee a good
answer. Evaluation checks answer quality, observability shows runtime behavior,
and cost controls help keep the feature sustainable.
```

## Interview Talking Points

- AI evaluation complements unit and integration tests.
- Observability should include model latency, token usage, fallback rate, and parse failures.
- Sensitive prompts and responses should not be logged directly.
- Cost and latency are part of AI feature design.
- Prompt versions and source ids make incidents easier to investigate.
