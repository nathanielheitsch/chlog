from typing import Any, Callable, List


class AIProviderInterface:
    async def openAISummarize(self, diff: List[str], cb: Callable[[str], Any]) -> str:
        """Call AI Provider to summarize diff"""
        pass
