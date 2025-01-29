from signalbot import Command, Context, SignalBot

from .chat import relay_message_to_ollama
from .config import BotConfig, OllamaConfig, SignalConfig

signal_config = SignalConfig()
ollama_config = OllamaConfig()
bot_config = BotConfig()


class BotCommand(Command):
    async def handle(self, c: Context):
        if c.message.text and c.message.text.lower().replace(",", "").startswith(bot_config.wake_word):
            response = await relay_message_to_ollama(c.message.text, ollama_config.context)
            await c.start_typing()
            await c.send(response)
            await c.stop_typing()


if __name__ == "__main__":
    bot = SignalBot(
        {
            "signal_service": signal_config.service,
            "phone_number": signal_config.number,
        }
    )
    bot.register(BotCommand())
    bot.start()
