from typing import cast
import aiohttp

from .config import AppConfig

config = AppConfig()


async def get_access_token(session):
    data = {
        "grant_type": "client_credentials"
    }
    auth = aiohttp.BasicAuth(config.icd.client_id, config.icd.client_secret)
    async with session.post(config.icd.request_token_url, data=data, auth=auth) as response:
        response_data = await response.json()
        return response_data.get("access_token")


async def fetch_icd_code_description(code: str, lang: str = "en") -> str:
    url = f"{config.icd.base_url}/icd/release/10/2019/{code}"
    headers = {
        "Accept": "application/json",
        "API-Version": "v2",
        "Accept-Language": lang
    }

    async with aiohttp.ClientSession() as session:
        token = await get_access_token(session)
        headers["Authorization"] = f"Bearer {token}"
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return cast(str, data["definition"]["@value"])


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(fetch_icd_code_description("F20.2")))  # noqa: T201
