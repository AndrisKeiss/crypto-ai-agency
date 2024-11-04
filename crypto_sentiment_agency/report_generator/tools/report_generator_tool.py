from agency_swarm.tools import BaseTool
from pydantic import Field
from datetime import datetime

class ReportGeneratorTool(BaseTool):
    """
    A tool for generating comprehensive cryptocurrency reports that combine market data and sentiment analysis.
    """
    
    price_data: dict = Field(
        ..., 
        description="Dictionary containing price and market data for multiple cryptocurrencies"
    )
    
    sentiment_data: dict = Field(
        ..., 
        description="Dictionary containing sentiment analysis data for multiple cryptocurrencies"
    )

    def format_number(self, value, is_price=False, is_percentage=False):
        """Safely formats numbers with proper handling of potential string/None values"""
        try:
            if value is None or value == 'N/A':
                return 'N/A'
            num = float(value)
            if is_price:
                return f"${num:,.2f}"
            if is_percentage:
                return f"{num:.2f}%"
            if num > 1_000_000:
                return f"${num:,.0f}"
            return f"{num:.2f}"
        except (ValueError, TypeError):
            return 'N/A'

    def run(self):
        """
        Generates a structured report combining price and sentiment data for each cryptocurrency.
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate individual crypto analyses
        crypto_analyses = []
        for crypto_id, sentiment_info in self.sentiment_data.items():
            if crypto_id in self.price_data:
                crypto_analyses.append(self.generate_single_crypto_analysis(crypto_id))
        
        report = f"""# Cryptocurrency Market & Sentiment Analysis Report
Date: {current_date}

## Analysis Scope
- Data sources: CoinGecko API (market data), Reddit (sentiment analysis)
- Time period: Past 24 hours
- Total Reddit posts analyzed: {self.get_total_posts()}

{' '.join(crypto_analyses)}

## Market Summary
{self.generate_market_summary()}

## Risk Assessment
{self.assess_overall_risks()}"""

        return report

    def generate_single_crypto_analysis(self, crypto_id):
        """Generates analysis for a single cryptocurrency"""
        price_info = self.price_data[crypto_id]
        sentiment_info = self.sentiment_data[crypto_id]
        symbol = crypto_id.upper()
        
        return f"""## {symbol} Analysis
### Market & Sentiment Metrics
- Current Price: {self.format_number(price_info.get('current_price'), is_price=True)}
- 24h Change: {self.format_number(price_info.get('price_change_24h'), is_percentage=True)}
- Trading Volume: {self.format_number(price_info.get('volume_24h'))}
- Reddit Mentions: {sentiment_info.get('mentions', 'N/A')}
- Sentiment Score: {self.format_number(sentiment_info.get('sentiment'))} (-1 to +1 scale)
- Market Mood: {self.get_market_mood(price_info, sentiment_info)}

### Key Insights
{self.generate_integrated_analysis(crypto_id, price_info, sentiment_info)}

### Trading Implications
{self.generate_trading_implications(price_info, sentiment_info)}

"""

    def get_market_mood(self, price_info, sentiment_info):
        """Determines market mood based on price and sentiment data"""
        try:
            sentiment_score = float(sentiment_info.get('sentiment', 0))
            price_change = float(price_info.get('price_change_24h', 0))
            
            if sentiment_score > 0.5 and price_change > 2:
                return "Strongly Bullish"
            elif sentiment_score > 0.2 and price_change > 0:
                return "Moderately Bullish"
            elif sentiment_score < -0.5 and price_change < -2:
                return "Strongly Bearish"
            elif sentiment_score < -0.2 and price_change < 0:
                return "Moderately Bearish"
            else:
                return "Neutral"
        except (ValueError, TypeError):
            return "Neutral"

    def generate_integrated_analysis(self, crypto_id, price_info, sentiment_info):
        """Generates integrated analysis combining price and sentiment metrics"""
        try:
            price_change = float(price_info.get('price_change_24h', 0))
            sentiment_score = float(sentiment_info.get('sentiment', 0))
            mentions = int(sentiment_info.get('mentions', 0))
            
            analysis = []
            
            # Price-sentiment correlation
            if abs(price_change) > 2:
                if (price_change > 0 and sentiment_score > 0) or (price_change < 0 and sentiment_score < 0):
                    analysis.append(f"- Strong alignment between price movement ({price_change:.1f}%) and sentiment ({sentiment_score:.2f})")
                else:
                    analysis.append(f"- Divergence between price ({price_change:.1f}%) and sentiment ({sentiment_score:.2f})")
            
            # Social engagement
            if mentions > 100:
                analysis.append(f"- High social engagement ({mentions} Reddit mentions)")
            elif mentions > 50:
                analysis.append(f"- Moderate social engagement ({mentions} Reddit mentions)")
            
            return "\n".join(analysis) if analysis else "- No significant patterns detected"
        except (ValueError, TypeError):
            return "- Unable to analyze due to data format issues"

    def generate_trading_implications(self, price_info, sentiment_info):
        """Generates trading implications based on combined analysis"""
        try:
            sentiment_score = float(sentiment_info.get('sentiment', 0))
            price_change = float(price_info.get('price_change_24h', 0))
            
            if sentiment_score > 0.5 and price_change > 2:
                return "- Strong buy signal: Positive sentiment with upward price momentum"
            elif sentiment_score < -0.5 and price_change < -2:
                return "- Consider reducing exposure: Negative sentiment with bearish price action"
            elif abs(sentiment_score - price_change/10) > 0.5:
                return "- Watch for potential trend reversal: Price-sentiment divergence"
            else:
                return "- Neutral conditions suggest maintaining current positions"
        except (ValueError, TypeError):
            return "- Insufficient data for trading recommendations"

    def get_total_posts(self):
        """Calculates total posts analyzed across all cryptocurrencies"""
        return sum(info.get('mentions', 0) for info in self.sentiment_data.values())

    def generate_market_summary(self):
        """Generates overall market summary"""
        try:
            total_mentions = self.get_total_posts()
            analyzed_coins = len([k for k in self.sentiment_data.keys() if k in self.price_data])
            
            return f"""- Analyzed {analyzed_coins} cryptocurrencies
- Total social mentions: {total_mentions}
- Market Activity Level: {'High' if total_mentions > 200 else 'Moderate' if total_mentions > 100 else 'Low'}"""
        except (ValueError, TypeError):
            return "Unable to generate market summary due to data format issues"

    def assess_overall_risks(self):
        """Assesses overall market risks"""
        risks = []
        try:
            # Sentiment divergence risk
            sentiment_values = [float(info.get('sentiment', 0)) for info in self.sentiment_data.values()]
            if sentiment_values and max(sentiment_values) - min(sentiment_values) > 0.5:
                risks.append("- High sentiment divergence across cryptocurrencies")
            
            # Price volatility risk
            price_changes = [float(info.get('price_change_24h', 0)) for info in self.price_data.values()]
            if price_changes and max(price_changes) - min(price_changes) > 5:
                risks.append("- Significant price volatility across assets")
            
            return "\n".join(risks) if risks else "- No significant market-wide risks identified"
        except (ValueError, TypeError):
            return "- Unable to assess risks due to data format issues"

if __name__ == "__main__":
    # Test data
    price_data = {
        "bitcoin": {
            "current_price": 68794,
            "price_change_24h": 0.56,
            "volume_24h": 1361606313591,
            "market_cap": 1361606313591
        }
    }
    
    sentiment_data = {
        "bitcoin": {
            "mentions": 253,
            "sentiment": 0.229
        }
    }
    
    tool = ReportGeneratorTool(
        price_data=price_data,
        sentiment_data=sentiment_data
    )
    print(tool.run()) 