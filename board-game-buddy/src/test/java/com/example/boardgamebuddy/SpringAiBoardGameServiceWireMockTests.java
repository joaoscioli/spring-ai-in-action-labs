package com.example.boardgamebuddy;


import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.tomakehurst.wiremock.client.ResponseDefinitionBuilder;
import com.github.tomakehurst.wiremock.client.WireMock;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.io.Resource;
import org.wiremock.spring.ConfigureWireMock;
import org.wiremock.spring.EnableWireMock;
import java.io.IOException;
import java.nio.charset.Charset;

@EnableWireMock(
        @ConfigureWireMock(baseUrlProperties = "openai.base.url"))
@SpringBootTest(
        properties = {
                "spring.ai.openai.base-url=${openai.base.url}",
                "spring.ai.azure.openai.chat.enabled=false",
                "spring.ai.ollama.chat.enabled=false"
        })
public class SpringAiBoardGameServiceWireMockTests {

    @Value("classpath:/test-openai-response.json")
    Resource responseResource;

    @Autowired
    ChatClient.Builder chatClientBuilder;

    @BeforeEach
    public void setup() throws IOException {
        var cannedResponse =
                responseResource.getContentAsString(Charset.defaultCharset());
        var mapper = new ObjectMapper();
        var responseNode = mapper.readTree(cannedResponse);
        WireMock.stubFor(WireMock.post("/v1/chat/completions")
                .willReturn(ResponseDefinitionBuilder.okForJson(responseNode)));
    }

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"", " ", "\n\t"})
    void returnsAnExplicitFallbackWhenTheProviderReturnsNoText(String content) throws IOException {
        var mapper = new ObjectMapper();
        var responseNode = mapper.readTree(responseResource.getContentAsString(Charset.defaultCharset()));
        var message = (com.fasterxml.jackson.databind.node.ObjectNode)
                responseNode.path("choices").get(0).path("message");
        message.put("content", content);
        WireMock.stubFor(WireMock.post("/v1/chat/completions")
                .willReturn(ResponseDefinitionBuilder.okForJson(responseNode)));

        var boardGameService = new SpringAiBoardGameService(chatClientBuilder);
        var answer = boardGameService.askQuestion(new Question("How many players can play Catan?"));

        Assertions.assertThat(answer.answer()).isEqualTo(SpringAiBoardGameService.EMPTY_RESPONSE_FALLBACK);
    }

    @Test
    public void testAskQuestion() {
        var boardGameService =
                new SpringAiBoardGameService(chatClientBuilder);
        var answer =
                boardGameService.askQuestion(
                        new Question("What is the capital of France?"));
        Assertions.assertThat(answer).isNotNull();
        Assertions.assertThat(answer.answer()).isEqualTo("Paris");

        WireMock.verify(WireMock.postRequestedFor(WireMock.urlEqualTo("/v1/chat/completions"))
                .withRequestBody(WireMock.containing(SpringAiBoardGameService.SYSTEM_PROMPT_VERSION))
                .withRequestBody(WireMock.containing("Answer only board game questions"))
                .withRequestBody(WireMock.containing("If the user asks about another topic"))
                .withRequestBody(WireMock.containing("Prefer concise answers with rules references")));
    }
}
