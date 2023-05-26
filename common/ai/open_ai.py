import asyncio
import logging
from typing import Any, Callable, List
import aiohttp

from .ai_provider_interface import AIProviderInterface


class OpenAIProvider(AIProviderInterface):

    def __init__(self, token: str) -> None:
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
        logging.debug(f'Using API Key: {token}')

    async def openAISummarize(self, diffs: List[str], cb: Callable[[str], Any]) -> str:
        logging.debug("starting summarize")

        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

        async def summarize(diff: str) -> str:
            async with semaphore, aiohttp.ClientSession() as session:
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a code changelog creator - you take in git diffs and provide a helpful list of changes."},
                        {"role": "user", "content": "Return a bulleted list describing the effects of the code changes in this git diff:\n\n" + diff},
                    ],
                    "max_tokens": 1200,
                    "temperature": 0
                }

                try:
                    async with session.post(self.url, headers=self.headers, json=data) as response:
                        parsed = await response.json()
                        out = parsed['choices'][0]['message']['content']
                        while out.startswith("\n"):
                            out = out[1:]
                        while out.endswith("\n"):
                            out = out[:-1]
                        out = f"\n{out}"
                        cb(out)
                        return out
                except Exception as e:
                    logging.error(e)

        # Create a list to hold the futures
        futures = []

        # Iterate through the diffs and schedule the summarize tasks
        for diff in diffs:
            future = asyncio.ensure_future(summarize(diff))
            futures.append(future)

        # Wait for all tasks to complete
        await asyncio.gather(*futures)
