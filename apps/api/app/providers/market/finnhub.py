from app.core.logger import setup_logger
import httpx
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

logger = setup_logger(__name__)


class FinnhubProvider(MarketDataProvider):
    """
    Finnhub API Provider.
    Implements get_quote using the /quote endpoint.
    Other endpoints are stubbed out for future implementation.
    """
    
    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self):
        self.api_key = settings.finnhub_api_key

    def get_quote(self, symbol: str) -> Quote:
        if not self.api_key:
            raise ProviderUnavailableError("Finnhub API key is not configured.")
            
        logger.info(f"Fetching quote for {symbol} using Finnhub")
        
        url = f"{self.BASE_URL}/quote"
        params = {
            "symbol": symbol,
            "token": self.api_key
        }
        
        try:
            response = httpx.get(url, params=params, timeout=10)
            
            # Finnhub returns 429 for rate limit exceeded
            if response.status_code == 429:
                raise ProviderUnavailableError("Finnhub API limit reached")
                
            response.raise_for_status()
            data = response.json()
            
            # If the symbol is invalid, Finnhub returns 0 for current price 'c' and null for others
            if data.get("c") == 0 and data.get("d") is None:
                raise SymbolNotFoundError(symbol)
                
            price = float(data["c"])
            
            return Quote(
                symbol=symbol,
                price=price,
                currency="USD", # Defaulting as Finnhub's /quote doesn't provide it
                source="finnhub"
            )
            
        except httpx.HTTPError as e:
            logger.error(f"Finnhub request failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Network error with Finnhub: {e}")
        except SymbolNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Finnhub parsing failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Parsing error with Finnhub: {e}")

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        raise ProviderUnavailableError("Historical prices not implemented for Finnhub yet.")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise ProviderUnavailableError("Company profile not implemented for Finnhub yet.")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        raise ProviderUnavailableError("Financial metrics not implemented for Finnhub yet.")
