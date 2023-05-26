class AIProviderInterface:
    async def openAISummarize(self, diff: str) -> str:
        """Call AI Provider to summarize diff"""
        pass