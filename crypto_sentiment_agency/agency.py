from agency_swarm import Agency
from report_generator.report_generator import ReportGenerator
from reddit_analyzer.reddit_analyzer import RedditAnalyzer

# Initialize agents with gpt-4-turbo-preview (the new name for gpt-4-0125-preview)
report_gen = ReportGenerator(
    model="gpt-4o-mini"  # Updated model name
)
reddit_analyzer = RedditAnalyzer(
    model="gpt-4o-mini"  # Updated model name
)

# Create agency with simplified communication flow
agency = Agency(
    [
        report_gen,  # Make Report Generator the main entry point
        [report_gen, reddit_analyzer],  # Report Generator can request sentiment data from Reddit Analyzer
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.5,
    max_prompt_tokens=25000
)

if __name__ == "__main__":
    agency.demo_gradio(
        height=900
    )