# Spring AI Fundamentals

This document summarizes the Spring AI concepts that matter most when building
AI-assisted backend features with Java and Spring Boot.

## What Spring AI Is

Spring AI is an application framework for AI engineering in the Spring
ecosystem. Its purpose is to help Spring applications connect enterprise data,
APIs, and application services with AI models while keeping familiar Spring
design principles such as portability, modularity, configuration, and POJO-based
application code.

## Core Building Blocks

### Model Client

A model client is the application boundary used to communicate with an AI model.

In backend design, this boundary should be treated like any other external
dependency:

- configure it explicitly;
- isolate it behind services;
- test application behavior around it;
- handle latency and failure;
- avoid leaking secrets.

### ChatClient

`ChatClient` provides a fluent API for chat-based model interactions.

It helps application code build a prompt from system and user messages, call the
model, and receive a response.

Good usage patterns:

- keep model interaction inside an application service;
- separate user input from system instructions;
- avoid placing business rules only inside prompts;
- define fallback behavior for unavailable models.

### Prompt

A prompt is the model input that guides response behavior.

For production-minded systems, prompts should be treated as part of the
application contract.

Good prompts should:

- define the role and task clearly;
- include only necessary context;
- set boundaries for unsafe or unsupported requests;
- request a response shape when structure matters;
- be versioned when changes can affect behavior.

### Structured Output

Structured output maps model responses into a predictable format, such as a Java
record or DTO.

This matters because backend services usually need data they can validate and
process, not only free-form text.

Use structured output when:

- the response feeds another service;
- the API returns typed data;
- validation is required;
- downstream behavior depends on specific fields.

### Advisors

Advisors can intercept, modify, and enhance AI interactions.

They are useful for cross-cutting AI behavior such as:

- adding context;
- applying memory;
- validating responses;
- implementing reusable prompt patterns;
- observing model calls.

### Tool Calling

Tool calling lets a model request that the application execute a specific
capability.

The important security point: the model does not directly access application
APIs. The application receives a tool call request, validates it, executes the
allowed function, and returns the result.

Good tool calling design requires:

- narrow tool boundaries;
- input validation;
- authorization checks;
- audit logging for important actions;
- clear separation between read tools and write tools.

### Retrieval-Augmented Generation

Retrieval-augmented generation, often called RAG, adds relevant external
knowledge to a model request.

Use RAG when:

- the model needs private or current project data;
- the answer should be grounded in documents;
- sending all context in the prompt would be too large;
- answers need traceability to source material.

## Engineering Concerns

AI features introduce familiar backend concerns in a new shape:

- latency: model calls can be slower than normal service calls;
- cost: every model request may have a financial cost;
- reliability: models and providers can fail;
- privacy: prompts may contain sensitive data;
- observability: prompts, completions, tools, and tokens need careful monitoring;
- evaluation: behavior can regress even when code compiles.

## Portfolio Direction

Strong examples in this repository should show:

- a clear business scenario;
- a bounded model interaction;
- deterministic application logic around AI calls;
- tests for non-model behavior;
- safe handling of secrets;
- documentation of model, prompt, and operational trade-offs.

## Interview Talking Points

- Spring AI brings AI features into familiar Spring Boot architecture.
- `ChatClient` is an application boundary, not a place to hide business rules.
- Prompts should be designed, reviewed, and evolved deliberately.
- Structured output makes AI responses easier to validate.
- Tool calling requires authorization and validation because it can trigger real application behavior.
- Observability and evaluation are part of responsible AI engineering.
