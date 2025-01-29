import aiohttp

from .config import OllamaConfig

ollama_config = OllamaConfig()


async def relay_message_to_ollama(message: str, context: str = "") -> str:
    url = f"http://{ollama_config.host}/api/generate/"
    payload = {
        "model": ollama_config.model,
        "prompt": f"{context}\n{message}",
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()

    return data.get("response", "")


# Example usage
if __name__ == "__main__":
    import asyncio

    message = "Why is the sky blue?"
    response = asyncio.run(relay_message_to_ollama(message, ollama_config.context))
    print(response)
