from agency_swarm import Agent
from .tools.reddit_sentiment_tool import RedditSentimentTool

class RedditAnalyzer(Agent):
    def __init__(self, model="gpt-4-turbo-preview"):
        super().__init__(
            name="Reddit Analyzer",
            description="Specialized agent for analyzing Reddit sentiment about cryptocurrencies.",
            instructions="./instructions.md",
            tools=[RedditSentimentTool],
            temperature=0.3,
            max_prompt_tokens=25000,
            model=model
        )