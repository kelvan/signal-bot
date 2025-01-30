from signalbot import Command, Context, SignalBot

from .chat import relay_message_to_ollama
from .config import AppConfig

config = AppConfig()


class BotCommand(Command):
    async def handle(self, c: Context):
        for personality in config.bot.personalities:
            msg = c.message.text
            if msg and msg.lower().replace(",", "").startswith(personality.trigger):
                response = await relay_message_to_ollama(msg, personality.model, personality.instructions)
                await c.start_typing()
                await c.send(response)
                await c.stop_typing()


if __name__ == "__main__":
    bot = SignalBot(
        {
            "signal_service": config.signal.service,
            "phone_number": config.signal.number,
        }
    )
    bot.register(BotCommand())
    bot.start()
