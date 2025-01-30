from typing import ClassVar

from confz import BaseConfig, ConfigSource, FileSource
from pydantic import BaseModel


class PersonalityConfig(BaseModel):
    trigger: str = "hey ollama"
    name: str = "Ollama"
    model: str = "llama3.2"
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


class AppConfig(BaseConfig):
    bot: BotConfig
    signal: SignalConfig
    ollama: OllamaConfig

    CONFIG_SOURCES: ClassVar[list[ConfigSource]] = [FileSource(file="config.yml")]
