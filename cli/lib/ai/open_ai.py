import json
import logging
import os
from typing import Any, Callable
import aiohttp

from .ai_provider_interface import AIProviderInterface
from cli.lib.consts import TOKEN_ENV_NAME


class OpenAIProvider(AIProviderInterface):

    def __init__(self) -> None:
        self.url = "https://api.openai.com/v1/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(os.getenv(TOKEN_ENV_NAME))
        }
        logging.debug(f'Using API Key: {os.getenv(TOKEN_ENV_NAME)}')

    async def openAISummarize(self, diff: str, cb: Callable[[str], Any]) -> str:
        logging.debug("starting summarize")
        data = {
            "model": "text-davinci-003",
            "prompt": [
                "Create a consise changelog for this git diff",
                diff
            ],
            "max_tokens": 1200,
            "temperature": 0
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(data)) as response:
                parsed = await response.json()
                out = parsed['choices'][0]['text']
                cb(out)
                return out
