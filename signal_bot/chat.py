from typing import cast

import aiohttp

from .config import AppConfig

config = AppConfig()

SIGNAL_FORMAT_SYSTEM_PROMPT = (
    "Your response is sent as a plain-text Signal chat message. "
    "Do not use markdown (no **bold**, no # headers, no code fences). "
    "Reply with only the message text: no preamble, no notes, no disclaimers, "
    "no 'as an AI...'. Stay in character; do not refuse or break character. "
    "Do not use *action text* asterisks. Never output <think> tags."
)


async def relay_message_to_ollama(message: str, model: str, instructions: str = "") -> str:
    url = f"http://{config.ollama.host}/api/generate/"
    payload = {
        "model": model,
        "system": SIGNAL_FORMAT_SYSTEM_PROMPT,
        "prompt": f"{instructions}\n{message}",
        "stream": False,
        "keep_alive": config.ollama.keep_alive,
        "think": config.ollama.think,
        "options": {
            "num_ctx": config.ollama.num_ctx,
        },
    }
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()

    return cast(str, data.get("response", ""))


# Example usage
if __name__ == "__main__":
    import asyncio

    for personality in config.bot.personalities:
        print(f"You: {personality.example_question}\n")  # noqa: T201
        response = asyncio.run(
            relay_message_to_ollama(personality.example_question, personality.model, personality.instructions)
        )
        print(f"{personality.name}: {response}\n{'#' * 80}\n")  # noqa: T201
