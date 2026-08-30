from app.core.logger import setup_logger
import re
import httpx
from datetime import date
from decimal import Decimal

from app.core.config import settings
from app.core.errors import ProviderUnavailableError
from app.providers.market.base import MarketDataProvider
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)

logger = setup_logger(__name__)


class TavilyProvider(MarketDataProvider):
    """
    An API-less fallback provider using Tavily Search API.
    This uses heuristics to extract price data from search results.
    It does not support historical data or deep financial metrics.
    """
    
    BASE_URL = "https://api.tavily.com/search"

    def __init__(self):
        self.api_key = settings.tavily_api_key

    def get_quote(self, symbol: str) -> Quote:
        if not self.api_key:
            raise ProviderUnavailableError("Tavily API key is not configured.")
            
        logger.info(f"Fetching quote for {symbol} using Tavily search fallback")
        query = f"{symbol} stock price"
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": True
        }
        
        try:
            response = httpx.post(self.BASE_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Try to extract from the generated answer first
            answer = data.get("answer", "")
            if answer:
                price = self._extract_price(answer)
                if price:
                    return Quote(
                        symbol=symbol,
                        price=float(price),
                        currency="USD",
                        source="tavily"
                    )
            
            # Fallback to search snippets
            results = data.get("results", [])
            for result in results:
                snippet = result.get("content", "")
                price = self._extract_price(snippet)
                if price:
                    return Quote(
                        symbol=symbol,
                        price=float(price),
                        currency="USD",
                        source="tavily"
                    )
            
            raise ProviderUnavailableError(f"Could not extract price for {symbol} from Tavily")
            
        except httpx.HTTPError as e:
            logger.error(f"Tavily request failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Network error with Tavily: {e}")
        except Exception as e:
            logger.error(f"Tavily parsing failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"Parsing error with Tavily: {e}")

    def _extract_price(self, text: str) -> Decimal | None:
        """
        Attempt to extract a stock price from unstructured text.
        """
        if not text:
            return None
        matches = re.findall(r'(?:[₹$]|USD|INR)?\s*(\d+(?:,\d{3})*(?:\.\d{1,2})?)', text)
        for match in matches:
            try:
                clean_num = match.replace(',', '')
                return Decimal(clean_num)
            except Exception:
                continue
        return None

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        logger.warning(f"TavilyProvider cannot fetch historical prices for {symbol}")
        raise ProviderUnavailableError("Historical prices not supported by Tavily fallback")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        logger.warning(f"TavilyProvider cannot fetch company profile for {symbol}")
        raise ProviderUnavailableError("Company profile not supported by Tavily fallback")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        logger.warning(f"TavilyProvider cannot fetch financial metrics for {symbol}")
        raise ProviderUnavailableError("Financial metrics not supported by Tavily fallback")
