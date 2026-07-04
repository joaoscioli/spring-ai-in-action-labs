package com.example.boardgamebuddy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AskController.class)
class AskControllerTests {

    @Autowired
    private MockMvc mockMvc;

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
    }
}
