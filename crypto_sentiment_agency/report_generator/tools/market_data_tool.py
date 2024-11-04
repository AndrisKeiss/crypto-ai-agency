from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class MarketDataTool(BaseTool):
    """
    A tool for fetching cryptocurrency market data using the CoinGecko API.
    """
    
    crypto_ids: List[str] = Field(
        ...,
        description="List of cryptocurrency IDs to fetch data for"
    )
    
    def run(self):
        """
        Fetch current market data for specified cryptocurrencies.
        Returns price, 24h change, and 7d change.
        """
        base_url = "https://api.coingecko.com/api/v3"
        
        # Join crypto IDs for the API call
        ids = ','.join(self.crypto_ids)
        
        # Using coins/markets endpoint with all required parameters
        params = {
            'vs_currency': 'usd',
            'ids': ids,
            'order': 'market_cap_desc',
            'per_page': len(self.crypto_ids),
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h,7d'
        }
        
        try:
            response = requests.get(
                f"{base_url}/coins/markets",
                params=params,
                headers={
                    'accept': 'application/json',
                    'x-cg-demo-api-key': os.getenv('COINGECKO_API_KEY', '')
                }
            )
            
            if response.status_code == 429:
                print("Rate limit reached. Please wait before trying again.")
                return None
                
            response.raise_for_status()
            
            data = response.json()
            market_data = {}
            
            for coin in data:
                market_data[coin['id']] = {
                    'current_price': coin['current_price'],
                    'price_change_24h': f"{coin.get('price_change_percentage_24h', 'N/A'):.2f}%" if coin.get('price_change_percentage_24h') is not None else "N/A",
                    'price_change_7d': f"{coin.get('price_change_percentage_7d_in_currency', 'N/A'):.2f}%" if coin.get('price_change_percentage_7d_in_currency') is not None else "N/A",
                    'market_cap': coin.get('market_cap', 'N/A'),
                    'last_updated': coin.get('last_updated', 'N/A')
                }
                
            return market_data
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching market data: {str(e)}")
            return None

if __name__ == "__main__":
    # Test with multiple cryptocurrencies
    tool = MarketDataTool(crypto_ids=['bitcoin', 'ethereum', 'solana', 'cardano'])
    results = tool.run()
    
    if results:
        print("\nMarket data for selected cryptocurrencies:")
        for crypto_id, data in results.items():
            print(f"\n{crypto_id}:")
            print(f"  Price: ${data['current_price']:,.2f}")
            print(f"  24h Change: {data['price_change_24h']}")
            print(f"  7d Change: {data['price_change_7d']}")
            print(f"  Market Cap: ${data['market_cap']:,.2f}")
            print(f"  Last Updated: {data['last_updated']}")
