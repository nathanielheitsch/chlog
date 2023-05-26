import asyncio
from enum import Enum
from typing import Any, AsyncGenerator, Callable, List

from lib.ai.ai_provider_enum import AIProvider
from lib.ai.open_ai import OpenAIProvider
from .consts import TOKEN_ENV_NAME


class AIService:
    def __init__(self, provider: AIProvider = AIProvider.OPENAI) -> None:
        pass
        match provider:
            case 1:
                self.ai = OpenAIProvider()
            case _:
                self.ai = OpenAIProvider()

    async def processDiffs(self, diffs: List[str], cb: Callable[[str], Any]) -> AsyncGenerator[str, str]:
        aiCalls = [self.ai.openAISummarize(diff, cb) for diff in diffs]
        await asyncio.gather(*aiCalls)
