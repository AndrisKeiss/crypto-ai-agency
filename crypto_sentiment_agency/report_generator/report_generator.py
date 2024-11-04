from agency_swarm import Agent
from .tools.market_data_tool import MarketDataTool
from .tools.report_generator_tool import ReportGeneratorTool

class ReportGenerator(Agent):
    def __init__(self, model="gpt-4-turbo-preview"):
        super().__init__(
            name="Report Generator",
            description="Specialized agent for generating comprehensive cryptocurrency analysis reports combining market data and sentiment analysis.",
            instructions="./instructions.md",
            tools=[MarketDataTool, ReportGeneratorTool],
            temperature=0.3,
            max_prompt_tokens=25000,
            model=model
        ) 