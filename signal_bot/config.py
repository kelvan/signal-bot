from confz import BaseConfig, EnvSource


class BotConfig(BaseConfig):
    wake_word: str = "hey ollama"

    CONFIG_SOURCES = [EnvSource(file=".env", prefix="BOT_", allow_all=True)]


class SignalConfig(BaseConfig):
    number: str
    service: str = "127.0.0.1:8080"

    CONFIG_SOURCES = [EnvSource(file=".env", prefix="SIGNAL_", allow_all=True)]


class OllamaConfig(BaseConfig):
    host: str = "127.0.0.1:11434"
    model: str = "llama3.2"
    context: str = ""

    CONFIG_SOURCES = [EnvSource(file=".env", prefix="OLLAMA_", allow_all=True)]
