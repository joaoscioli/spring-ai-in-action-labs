# AI Safety Checklist

Use this checklist before presenting an AI feature as portfolio-ready.

## Input Safety

- user input has length limits;
- prompt injection risks are considered;
- sensitive data is minimized before model calls;
- uploaded or retrieved documents have ownership and access controls.

## Output Safety

- structured output is validated;
- unsupported answers have a fallback;
- the model is instructed to admit missing information;
- user-facing text avoids unsupported guarantees.

## Tool Safety

- tools are narrow;
- inputs are validated;
- authorization is checked before execution;
- write-capable tools require extra review;
- important tool calls are audited.

## RAG Safety

- retrieval is scoped by authorization;
- source metadata is preserved;
- private documents are not logged;
- answers cite sources when required;
- missing context is handled explicitly.

## Operational Safety

- latency has a timeout;
- cost is tracked;
- provider errors have fallbacks;
- logs avoid secrets and sensitive prompts;
- prompt versions are traceable.

## Interview Talking Points

- AI safety is an engineering responsibility.
- Tool calling increases risk if authorization is weak.
- RAG needs access control before retrieval context reaches the model.
- Fallback behavior should be designed before demos.
