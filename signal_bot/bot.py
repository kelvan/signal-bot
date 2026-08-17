import logging

from signalbot import Config, DataMessageContext, DataMessageHandler, SendMessage, SignalBot

from .chat import relay_message_to_ollama
from .config import AppConfig, PersonalityConfig
from .icd import fetch_icd_code_description

config = AppConfig()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotCommand(DataMessageHandler):
    async def handle_data_message(self, context: DataMessageContext) -> None:
        msg = context.message.text
        personalities = [
            PersonalityConfig(
                name="icd10",
                trigger="hey icd10",
            ),
            *config.bot.personalities,
        ]

        if not msg:
            return

        logger.info(f"Received message: {msg}")

        cleaned_msg = msg.lower().replace(",", "")
        if cleaned_msg.startswith("hey bot"):
            cmd = cleaned_msg.split(" ", 2)[2]
            if cmd == "list":
                await context.reply(
                    SendMessage(
                        text="\n".join([f"{p.name}: {p.trigger}" for p in personalities])
                    )
                )
                return

        if cleaned_msg.startswith("hey icd10"):
            await context.start_typing()
            try:
                icd_code = cleaned_msg.split(" ", 3)[2].upper()
                description = await fetch_icd_code_description(icd_code)
                if len(splitted := cleaned_msg.split(" ", 3)) == 4:
                    question = splitted[3]
                else:
                    question = "Tell me about yourself."
                instructions = f"""
                    You are a patient in a psychiatric hospital.
                    Keep your responses short.
                    {question}
                    Do not mention your condition, just act like a person with the condition.
                    You have a mental condition, you should act on, with the following description of your condition:
                    {description}
                """
                response = await relay_message_to_ollama(msg, "qwen3.5:4b", instructions)
                await context.reply(SendMessage(text=response))
            finally:
                await context.stop_typing()
            return

        for personality in personalities:
            if cleaned_msg.startswith(personality.trigger):
                await context.start_typing()
                try:
                    response = await relay_message_to_ollama(
                        msg, personality.model, personality.instructions
                    )
                    await context.reply(SendMessage(text=response))
                finally:
                    await context.stop_typing()


if __name__ == "__main__":
    bot = SignalBot(
        Config(
            signal_service=config.signal.service,
            phone_number=config.signal.number,
        )
    )
    bot.register(BotCommand())
    bot.start()
