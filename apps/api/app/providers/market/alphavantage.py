import logging
import requests
from datetime import date

from app.core.config import settings
from app.core.errors import ProviderUnavailableError, SymbolNotFoundError
from app.providers.market.base import MarketDataProvider
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)

logger = logging.getLogger(__name__)


class AlphaVantageProvider(MarketDataProvider):
    """
    Alpha Vantage API Provider.
    Implements get_quote using the GLOBAL_QUOTE endpoint.
    Other endpoints are stubbed out for future implementation.
    """
    
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = settings.alpha_vantage_api_key

    def get_quote(self, symbol: str) -> Quote:
        if not self.api_key:
            raise ProviderUnavailableError("Alpha Vantage API key is not configured.")
            
        logger.info(f"Fetching quote for {symbol} using Alpha Vantage")
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Alpha Vantage might return an Information message on rate limits
            if "Information" in data or "Note" in data:
                raise ProviderUnavailableError(f"Alpha Vantage API limit reached: {data}")
                
            quote_data = data.get("Global Quote", {})
            if not quote_data or not quote_data.get("05. price"):
                # If there's no price, the symbol likely doesn't exist
                raise SymbolNotFoundError(symbol)
                
            price = float(quote_data["05. price"])
            
            return Quote(
                symbol=symbol,
                price=price,
                currency="USD", # Defaulting as AV doesn't provide it in GLOBAL_QUOTE
                source="alphavantage"
            )
            
        except requests.RequestException as e:
            logger.error(f"Alpha Vantage request failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Network error with Alpha Vantage: {e}")
        except SymbolNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Alpha Vantage parsing failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Parsing error with Alpha Vantage: {e}")

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        raise ProviderUnavailableError("Historical prices not implemented for Alpha Vantage yet.")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise ProviderUnavailableError("Company profile not implemented for Alpha Vantage yet.")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        raise ProviderUnavailableError("Financial metrics not implemented for Alpha Vantage yet.")
