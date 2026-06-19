package com.example.boardgamebuddy;

public record Question(String question) {
    public Question {
        if (question == null || question.isBlank()) {
            throw new IllegalArgumentException("question must not be blank");
        }
    }
}
