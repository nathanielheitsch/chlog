from typing import Any, Callable, List


class AIProviderInterface:
    async def chlog(self, diff: List[str], cb: Callable[[str], Any]) -> str:
        """Call AI Provider to summarize diff"""
        pass
    async def summarize(self, chlog: str, commit_messages: str) -> str:
        """Summarize the passed chlog"""
        pass
