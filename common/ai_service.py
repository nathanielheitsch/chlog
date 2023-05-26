import os
from typing import Any, Callable, List

from common.ai.ai_provider_enum import AIProvider
from common.ai.open_ai import OpenAIProvider

from .consts import TOKEN_ENV_NAME


class AIService:
    def __init__(self, token: str, provider: AIProvider = AIProvider.OPENAI) -> None:
        token = token if token else os.getenv(TOKEN_ENV_NAME)
        match provider:
            case 1:
                self.ai = OpenAIProvider(token)
            case _:
                self.ai = OpenAIProvider(token)

    async def processDiffs(self, diffs: List[str], cb: Callable[[str], Any]):
        await self.ai.openAISummarize(diffs, cb)
