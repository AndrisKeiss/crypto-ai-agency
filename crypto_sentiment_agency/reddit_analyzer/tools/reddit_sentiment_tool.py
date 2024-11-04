from agency_swarm.tools import BaseTool
from pydantic import Field
import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from collections import defaultdict
import os
import sys
from dotenv import load_dotenv
import yaml  # Add this import

load_dotenv()

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)

# Initialize spaCy with error handling
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy English language model...")
    os.system(f"{sys.executable} -m spacy download en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

# Load mappings from YAML
try:
    with open(os.path.join(os.path.dirname(__file__), 'crypto_mappings.yaml')) as f:
        CRYPTO_MAPPING = yaml.safe_load(f)
    print(f"Loaded {len(CRYPTO_MAPPING)} crypto mappings")
except FileNotFoundError:
    print("Error: crypto_mappings.yaml not found in the tools directory")
    print("Current directory:", os.path.dirname(__file__))
    raise

class RedditSentimentTool(BaseTool):
    """
    A tool for analyzing sentiment and trends from crypto-related subreddits.
    Uses PRAW for Reddit access and NLTK for sentiment analysis.
    """
    
    subreddits: str = Field(
        default="CryptoCurrency,Bitcoin",
        description="Comma-separated list of subreddits to analyze"
    )
    
    time_filter: str = Field(
        default="day",
        description="Time filter for posts (hour, day, week, month, year, all)"
    )
    
    limit: int = Field(
        default=100,
        description="Number of posts to analyze per subreddit"
    )

    def run(self):
        """
        Analyze Reddit posts and comments for crypto sentiment.
        Returns a dictionary of cryptocurrencies with their sentiment scores.
        """
        print("Initializing Reddit client...")
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'Crypto Sentiment Bot 1.0')
        )
        
        sia = SentimentIntensityAnalyzer()
        crypto_sentiment = defaultdict(lambda: {'mentions': 0, 'sentiment': 0.0})
        
        subreddit_list = self.subreddits.split(',')
        total_subreddits = len(subreddit_list)
        
        print(f"\nAnalyzing {total_subreddits} subreddits, {self.limit} posts each...")
        
        for idx, subreddit_name in enumerate(subreddit_list, 1):
            subreddit_name = subreddit_name.strip()
            print(f"\nProcessing r/{subreddit_name} ({idx}/{total_subreddits})")
            subreddit = reddit.subreddit(subreddit_name)
            
            posts_processed = 0
            for submission in subreddit.hot(limit=self.limit):
                posts_processed += 1
                if posts_processed % 10 == 0:  # Show progress every 10 posts
                    print(f"Processing posts: {posts_processed}/{self.limit}", end='\r')
                
                # Analyze post title and body
                text = f"{submission.title} {submission.selftext}"
                self._process_text(text, crypto_sentiment, sia)
                
                # Analyze top-level comments
                submission.comments.replace_more(limit=0)
                for comment in submission.comments[:10]:
                    self._process_text(comment.body, crypto_sentiment, sia)
            
            print(f"\nCompleted {posts_processed} posts from r/{subreddit_name}")
        
        print("\nCalculating final sentiment scores...")
        # Calculate average sentiment
        for crypto in crypto_sentiment:
            if crypto_sentiment[crypto]['mentions'] > 0:
                crypto_sentiment[crypto]['sentiment'] /= crypto_sentiment[crypto]['mentions']
        
        # Sort by mentions and sentiment
        sorted_cryptos = dict(sorted(
            crypto_sentiment.items(),
            key=lambda x: (x[1]['mentions'], x[1]['sentiment']),
            reverse=True
        ))
        
        print("Analysis complete!")
        return sorted_cryptos

    def _process_text(self, text, crypto_sentiment, sia):
        """Helper method to process text and update sentiment"""
        # Convert text to lowercase for matching
        text_lower = text.lower()
        
        # Look for cryptocurrency mentions
        for mention, canonical_name in CRYPTO_MAPPING.items():
            # Look for the mention as a whole word
            if f' {mention} ' in f' {text_lower} ':
                sentiment = sia.polarity_scores(text)['compound']
                crypto_sentiment[canonical_name]['mentions'] += 1
                crypto_sentiment[canonical_name]['sentiment'] += sentiment

if __name__ == "__main__":
    tool = RedditSentimentTool()
    results = tool.run()
    print("Top mentioned cryptocurrencies with sentiment:")
    for crypto, data in list(results.items())[:10]:
        print(f"{crypto}: {data['mentions']} mentions, sentiment: {data['sentiment']:.2f}") 