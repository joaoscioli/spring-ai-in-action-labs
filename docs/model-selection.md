# Model Selection

Model selection should be based on product needs and engineering constraints.

## Decision Factors

- answer quality;
- latency;
- cost;
- context window;
- structured output support;
- tool calling support;
- provider reliability;
- data handling requirements.

## Practical Rule

Use the smallest model that reliably satisfies the feature's quality bar.

Larger models may be useful for complex reasoning or nuanced generation, but
they can increase latency and cost. Small models can be enough for focused
classification, extraction, routing, or simple assistance.

## Evaluation Before Switching

Before changing a model:

- run the evaluation dataset;
- compare answer quality;
- compare latency;
- estimate cost impact;
- review safety behavior;
- document the decision.

## Portfolio Signal

This shows that AI engineering decisions are not made by hype. They are made by
balancing user value, reliability, cost, and operational constraints.
