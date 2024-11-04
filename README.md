# Crypto Sentiment Agency

A specialized AI agency that analyzes cryptocurrency market data and social sentiment to generate comprehensive market reports. The agency combines price data from CoinGecko with Reddit sentiment analysis to provide actionable insights.

## Features

- Real-time cryptocurrency price and market data analysis
- Reddit sentiment analysis across major crypto communities
- Integrated price-sentiment correlation analysis
- Trading implications based on combined metrics
- Risk assessment and market mood evaluation

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd crypto-sentiment-agency
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.env`:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## Usage

Run the agency using:
```bash
python crypto_sentiment_agency/agency.py
```

This will launch a Gradio interface where you can interact with the agency.

### Example Inputs

The agency is designed to understand natural language requests. Here are some example prompts:

1. Simple single-coin analysis:
```
Please prepare a report on Bitcoin
```

2. Multiple coin analysis:
```
Generate a report for Bitcoin and Ethereum
```

3. Specific aspect analysis:
```
Analyze the sentiment for Bitcoin in the last 24 hours
```

4. Market comparison:
```
Compare Bitcoin and Ethereum sentiment and price trends
```

### Sample Output

See `sample_output.txt` for an example of the detailed report format.

## How It Works

The agency consists of two specialized agents:

1. **Reddit Analyzer**
   - Analyzes sentiment from cryptocurrency subreddits
   - Processes posts and comments to generate sentiment scores
   - Identifies key discussion topics and trends

2. **Report Generator**
   - Fetches real-time market data from CoinGecko
   - Combines market data with sentiment analysis
   - Generates comprehensive analysis reports
   - Provides trading implications and risk assessment

### Report Structure

Each report includes:
- Analysis scope and metadata
- Per-cryptocurrency analysis
  - Price and market metrics
  - Sentiment analysis
  - Integrated insights
  - Trading implications
- Market-wide summary
- Risk assessment

## Limitations

- Reddit sentiment analysis is limited to English language posts
- Market data is refreshed every few minutes (CoinGecko API rate limits)
- Sentiment analysis covers the most recent 24-hour period
- Analysis is focused on major cryptocurrencies with significant social media presence

## Acknowledgments

This project is built using [Agency Swarm](https://github.com/VRSEN/agency-swarm/), an open-source framework for creating collaborative AI agents. Agency Swarm was created by Arsenii Shatokhin ([@VRSEN](https://github.com/VRSEN)) to enable the development of customizable and efficient AI agent systems. The framework provides the foundation for our agent communication, tool creation, and state management capabilities.