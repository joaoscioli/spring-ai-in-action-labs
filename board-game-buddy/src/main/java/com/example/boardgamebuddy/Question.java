package com.example.boardgamebuddy;

import jakarta.validation.constraints.NotBlank;

public record Question(
        @NotBlank(message = "question must not be blank")
        String question
) {
}
