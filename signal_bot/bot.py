from signalbot import Command, Context, SignalBot

from .chat import relay_message_to_ollama
from .config import AppConfig

config = AppConfig()


class BotCommand(Command):
    async def handle(self, c: Context):
        msg = c.message.text
        personalities = config.bot.personalities

        if not msg:
            return

        cleaned_msg = msg.lower().replace(",", "")
        if cleaned_msg.startswith("hey bot"):
            cmd = cleaned_msg.split(" ", 2)[2]
            if cmd == "list":
                await c.reply("\n".join([f"{p.name}: {p.trigger}" for p in personalities]))
                return

        for personality in personalities:
            if cleaned_msg.startswith(personality.trigger):
                response = await relay_message_to_ollama(msg, personality.model, personality.instructions)
                await c.start_typing()
                await c.reply(response)
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
