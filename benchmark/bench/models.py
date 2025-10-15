from dataclasses import dataclass

from openai import OpenAI, AzureOpenAI


@dataclass
class Prompt:
    message: str
    assistant: bool = False


class LanguageModel:
    def send_prompt(self, prompt: str | list[str | Prompt]) -> str:
        raise NotImplementedError()


class OpenAIModel(LanguageModel):
    def __init__(self, model):
        super().__init__()
        self.client = OpenAI()
        self.model = model

    def send_prompt(self, prompt: str | list[str | Prompt]) -> str:
        messages = []

        if isinstance(prompt, str):
            prompt = [prompt]

        for msg in prompt:
            if not isinstance(msg, Prompt):
                msg = Prompt(msg)

            messages.append(
                {
                    "role": "assistant" if msg.assistant else "user",
                    "content": msg.message,
                }
            )

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=0,
        )

        assert len(chat_completion.choices) == 1
        return chat_completion.choices[0].message.content


class GPT35Turbo(OpenAIModel):
    def __init__(self):
        super().__init__("gpt-3.5-turbo")


class GPT4(OpenAIModel):
    def __init__(self):
        super().__init__("gpt-4")


class GPT4Turbo(OpenAIModel):
    def __init__(self):
        super().__init__("gpt-4-0125-preview")


class Llama370b(OpenAIModel):
    def __init__(self):
        super().__init__("llama3:70b")


class Qwen3(OpenAIModel):
    def __init__(self):
        super().__init__("qwen3:32b")


class Phi3Mini(OpenAIModel):
    def __init__(self):
        super().__init__("phi3:mini")


class Phi3Medium(OpenAIModel):
    def __init__(self):
        super().__init__("phi3:medium")


class AzureOpenAIModel(OpenAIModel):
    def __init__(self, model):
        self.client = AzureOpenAI()
        self.model = model


class AzureGPT4(AzureOpenAIModel):
    def __init__(self):
        super().__init__("gpt-4")


class AzureGPT35Turbo(AzureOpenAIModel):
    def __init__(self):
        super().__init__("gpt-35-turbo")


class AzureGPT35Turbo16k(AzureOpenAIModel):
    def __init__(self):
        super().__init__("gpt-35-turbo-16k")


class AzureGPT4o(AzureOpenAIModel):
    def __init__(self):
        super().__init__("gpt-4o")
