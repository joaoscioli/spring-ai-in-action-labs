package com.example.boardgamebuddy;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AskController.class)
class AskControllerTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private BoardGameService boardGameService;

    @Test
    void askReturnsAnswerFromService() throws Exception {
        when(boardGameService.askQuestion(any(Question.class)))
                .thenReturn(new Anwser("Try Ticket to Ride for a light strategy game."));

        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "question": "What board game should I play with beginners?"
                                }
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.answer").value("Try Ticket to Ride for a light strategy game."));

        verify(boardGameService).askQuestion(new Question("What board game should I play with beginners?"));
    }

    @Test
    void askRejectsBlankQuestion() throws Exception {
        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "question": " "
                                }
                                """))
                .andExpect(status().isBadRequest());
        verifyNoInteractions(boardGameService);
    }

    @Test
    void askRejectsMissingQuestion() throws Exception {
        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isBadRequest());
        verifyNoInteractions(boardGameService);
    }

    @Test
    void askRejectsQuestionThatExceedsTheCostGuardrail() throws Exception {
        var oversizedQuestion = "a".repeat(501);

        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "question": "%s"
                                }
                                """.formatted(oversizedQuestion)))
                .andExpect(status().isBadRequest());
        verifyNoInteractions(boardGameService);
    }

    @Test
    void acceptsQuestionAtTheMaximumLength() throws Exception {
        var question = new Question("a".repeat(500));
        when(boardGameService.askQuestion(question)).thenReturn(new Anwser("Boundary accepted."));

        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(question)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.answer").value("Boundary accepted."));

        verify(boardGameService).askQuestion(question);
    }

    @ParameterizedTest
    @ValueSource(strings = {"{\"question\":null}", "{\"question\":\"\"}",
            "{\"question\":\"\\t\\n\"}", "null", "{invalid"})
    void rejectsInvalidBodiesBeforeCallingTheProvider(String body) throws Exception {
        mockMvc.perform(post("/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(boardGameService);
    }
}
