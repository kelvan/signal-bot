import re
from typing import cast

import aiohttp

from .config import AppConfig
from .language import detect_language_name

config = AppConfig()

SIGNAL_FORMAT_SYSTEM_PROMPT = (
    "Your response is sent as a plain-text Signal chat message. "
    "Do not use markdown (no **bold**, no # headers, no code fences). "
    "Reply with only the message text: no preamble, no notes, no disclaimers, "
    "no 'as an AI...'. Stay in character; do not refuse or break character. "
    "Do not use *action text* asterisks. Never output <think> tags. "
    "Keep answers short."
)


THINK_TAGS = re.compile(r"<think>.*?</think>", re.DOTALL)


async def _post_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            return cast(dict, await response.json())


async def _generate_ollama(prompt: str, model: str, temperature: float | None) -> str:
    options: dict[str, float | int] = {"num_ctx": config.ollama.num_ctx}
    if temperature is not None:
        options["temperature"] = temperature
    data = await _post_json(
        f"http://{config.ollama.host}/api/generate/",
        {
            "model": model,
            "system": SIGNAL_FORMAT_SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "keep_alive": config.ollama.keep_alive,
            "think": config.ollama.think,
            "options": options,
        },
        {},
    )
    return cast(str, data.get("response", ""))


async def _generate_openai(prompt: str, model: str, temperature: float | None) -> str:
    headers = {}
    if config.openai.api_key:
        headers["Authorization"] = f"Bearer {config.openai.api_key}"
    payload: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": SIGNAL_FORMAT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }
    if temperature is not None:
        payload["temperature"] = temperature
    data = await _post_json(
        f"{config.openai.base_url.rstrip('/')}/chat/completions",
        payload,
        headers,
    )
    content = cast(str, data["choices"][0]["message"].get("content") or "")
    return THINK_TAGS.sub("", content).strip()


def build_prompt(message: str, instructions: str, trigger: str) -> str:
    prompt = f"{instructions}\n{message}"
    content = message.lower().removeprefix(trigger.lower()) if trigger else message
    if language := detect_language_name(content.lstrip(" ,:;.!?")):
        prompt += (
            f"\n\n(Answer in {language}, "
            "unless your character instructions name another language or dialect.)"
        )
    return prompt


async def relay_message_to_llm(
    message: str,
    model: str,
    instructions: str = "",
    temperature: float | None = None,
    trigger: str = "",
) -> str:
    prompt = build_prompt(message, instructions, trigger)
    if temperature is None:
        temperature = config.llm.temperature
    if config.llm.backend == "openai":
        return await _generate_openai(prompt, model, temperature)
    return await _generate_ollama(prompt, model, temperature)


# Example usage
if __name__ == "__main__":
    import asyncio

    for personality in config.bot.personalities:
        print(f"You: {personality.example_question}\n")  # noqa: T201
        response = asyncio.run(
            relay_message_to_llm(
                personality.example_question,
                personality.model,
                personality.instructions,
                personality.temperature,
                personality.trigger,
            )
        )
        print(f"{personality.name}: {response}\n{'#' * 80}\n")  # noqa: T201
