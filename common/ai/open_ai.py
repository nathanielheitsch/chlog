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

    async def chlog(self, diffs: List[str], commit_messages: str, cb: Callable[[str], Any]) -> str:
        logging.debug("starting summarize")

        semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

        async def subchlog(diff: str) -> str:
            async with semaphore, aiohttp.ClientSession() as session:
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a code changelog creator - you take in git diffs and provide a helpful list of changes."},
                        {"role": "user", "content": "Here are the commit messages that may provide context to the code changes:\n\n" + commit_messages},
                        {"role": "user", "content": "Return a bulleted list describing the effects of the code changes in this git diff, if the changes are not consequential return nothing - ensure every line returned starts as a bullet:\n\n" + diff},
                    ],
                    "max_tokens": 1200,
                    "temperature": 0
                }

                try:
                    retry = 0
                    while retry <= 2:
                        async with session.post(self.url, headers=self.headers, json=data) as response:
                            parsed = await response.json()
                            try:
                                out = parsed['choices'][0]['message']['content']
                            except:
                               return 
                            retry = 3
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
            future = asyncio.ensure_future(subchlog(diff))
            futures.append(future)

        # Wait for all tasks to complete
        await asyncio.gather(*futures)

    async def summarize(self, chlog: str, commit_messages: str) -> str:
        async with aiohttp.ClientSession() as session:
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a code changelog summarizer - you take in a large changelog and summarize the important changes."},
                    {"role": "user", "content": f"Here are the commit messages that may provide context to the code changes:\n\n{commit_messages}"},
                    {"role": "user", "content": f"Return a shortened and consise version of this changelog - ensure to explain important changes:\n\n{chlog}"},
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
                    return out
            except Exception as e:
                logging.error(e)
