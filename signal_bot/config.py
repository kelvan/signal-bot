from typing import ClassVar, Literal

from confz import BaseConfig, ConfigSource, EnvSource, FileSource
from pydantic import BaseModel


class PersonalityConfig(BaseModel):
    trigger: str = "hey ollama"
    name: str = "Ollama"
    model: str = "gemma4:e2b"
    temperature: float | None = None
    instructions: str = """
        You are a Signal AI bot.
        You generate chat replies based on the prompt you receive.
        Be relevant and respectful.
    """
    example_question: str = "Why is the sky blue?"


class BotConfig(BaseModel):
    personalities: list[PersonalityConfig] = [PersonalityConfig()]


class SignalConfig(BaseModel):
    number: str
    service: str = "127.0.0.1:8080"


class OllamaConfig(BaseModel):
    host: str = "127.0.0.1:11434"
    context: str = ""
    keep_alive: int = -1
    think: bool = False
    num_ctx: int = 2048


class OpenAIConfig(BaseModel):
    base_url: str = "http://127.0.0.1:8000/v1"
    api_key: str = ""


class LLMConfig(BaseModel):
    backend: Literal["ollama", "openai"] = "ollama"
    temperature: float | None = None


class ICDConfig(BaseModel):
    base_url: str = "https://id.who.int/"
    request_token_url: str = "https://icdaccessmanagement.who.int/connect/token"
    client_id: str
    client_secret: str


class AppConfig(BaseConfig):
    bot: BotConfig
    signal: SignalConfig
    ollama: OllamaConfig = OllamaConfig()
    llm: LLMConfig = LLMConfig()
    openai: OpenAIConfig = OpenAIConfig()
    icd: ICDConfig

    CONFIG_SOURCES: ClassVar[list[ConfigSource]] = [
        FileSource(file="config.yml"),
        EnvSource(allow=["OLLAMA_HOST"], remap={"OLLAMA_HOST": "ollama.host"}),
    ]
