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


class FMPProvider(MarketDataProvider):
    """
    Financial Modeling Prep (FMP) API Provider.
    Implements get_quote using the /v3/quote endpoint.
    Other endpoints are stubbed out for future implementation.
    """
    
    BASE_URL = "https://financialmodelingprep.com/api/v3"

    def __init__(self):
        self.api_key = settings.fmp_api_key

    def get_quote(self, symbol: str) -> Quote:
        if not self.api_key:
            raise ProviderUnavailableError("FMP API key is not configured.")
            
        logger.info(f"Fetching quote for {symbol} using FMP")
        
        url = f"{self.BASE_URL}/quote/{symbol}"
        params = {
            "apikey": self.api_key
        }
        
        try:
            response = httpx.get(url, params=params, timeout=10)
            
            # FMP returns 429 for rate limit exceeded or 403 for invalid key
            if response.status_code in (403, 429):
                raise ProviderUnavailableError(f"FMP API access error: {response.status_code}")
                
            response.raise_for_status()
            data = response.json()
            
            # If the symbol is invalid, FMP returns an empty list
            if not data or len(data) == 0:
                raise SymbolNotFoundError(symbol)
                
            quote_data = data[0]
            price = float(quote_data["price"])
            
            return Quote(
                symbol=symbol,
                price=price,
                currency="USD", # FMP /quote is usually USD unless specified
                source="fmp"
            )
            
        except httpx.HTTPError as e:
            logger.error(f"FMP request failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Network error with FMP: {e}")
        except SymbolNotFoundError:
            raise
        except Exception as e:
            logger.error(f"FMP parsing failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Parsing error with FMP: {e}")

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        raise ProviderUnavailableError("Historical prices not implemented for FMP yet.")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise ProviderUnavailableError("Company profile not implemented for FMP yet.")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        raise ProviderUnavailableError("Financial metrics not implemented for FMP yet.")
