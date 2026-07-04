# Board Game Buddy API

`board-game-buddy` exposes a small HTTP API for asking board-game-related
questions through a Spring AI backed service.

## Ask A Question

```http
POST /ask
Content-Type: application/json
Accept: application/json
```

Request body:

```json
{
  "question": "What board game should I play with beginners?"
}
```

Successful response:

```json
{
  "answer": "Try Ticket to Ride for a light strategy game."
}
```

## Validation

The `question` field is required and must not be blank.

Invalid request:

```json
{
  "question": " "
}
```

Expected behavior:

- HTTP status: `400 Bad Request`
- the model is not called when the request is invalid

## Prompt Boundary

The service uses a system prompt that limits the assistant to board-game
questions. If the user asks about another topic, the assistant should explain
that it can only help with board games.

This boundary is covered by tests that verify the prompt instructions sent to
the model provider.
