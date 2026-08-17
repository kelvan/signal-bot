from typing import ClassVar

from confz import BaseConfig, ConfigSource, EnvSource, FileSource
from pydantic import BaseModel


class PersonalityConfig(BaseModel):
    trigger: str = "hey ollama"
    name: str = "Ollama"
    model: str = "qwen3.5:4b"
    instructions: str = """
        You are a Signal AI bot.
        You generate chat replies based on the prompt you receive.
        Keep your responses short, relevant and respectful.
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


class ICDConfig(BaseModel):
    base_url: str = "https://id.who.int/"
    request_token_url: str = "https://icdaccessmanagement.who.int/connect/token"
    client_id: str
    client_secret: str


class AppConfig(BaseConfig):
    bot: BotConfig
    signal: SignalConfig
    ollama: OllamaConfig
    icd: ICDConfig

    CONFIG_SOURCES: ClassVar[list[ConfigSource]] = [
        FileSource(file="config.yml"),
        EnvSource(allow=["OLLAMA_HOST"], remap={"OLLAMA_HOST": "ollama.host"}),
    ]
