# Implementation Examples

This document defines practical implementation examples for the Spring AI
Engineering Labs.

## Example 1: Billing Support Assistant

Feature:

- answer support questions using subscription context.

Engineering focus:

- prompt template;
- structured output;
- fallback behavior;
- no account mutation.

## Example 2: Documentation RAG Assistant

Feature:

- answer questions from approved documentation.

Engineering focus:

- document chunking;
- retrieval;
- source metadata;
- grounded answers;
- missing-information handling.

## Example 3: Read-Only Tool Calling

Feature:

- allow the model to request subscription status through a safe backend tool.

Engineering focus:

- tool input validation;
- authorization boundary;
- audit logging;
- no write actions in the first version.

## Example 4: Evaluation Harness

Feature:

- run a small set of expected questions against prompt versions.

Engineering focus:

- answer quality criteria;
- groundedness checks;
- latency notes;
- cost visibility.

## Interview Talking Points

- Examples are tied to business workflows.
- AI behavior stays behind service boundaries.
- Read-only tools are safer first steps.
- RAG should include source traceability.
- Evaluation turns demos into engineering practice.
