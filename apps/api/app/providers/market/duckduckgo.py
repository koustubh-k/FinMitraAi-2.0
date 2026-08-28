import logging
import re
from datetime import date
from decimal import Decimal

from duckduckgo_search import DDGS

from app.core.errors import ProviderUnavailableError
from app.providers.market.base import MarketDataProvider
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)

logger = logging.getLogger(__name__)


class DuckDuckGoProvider(MarketDataProvider):
    """
    An API-less fallback provider using DuckDuckGo web search.
    This uses heuristics to extract price data from search results.
    It does not support historical data or deep financial metrics.
    """

    def get_quote(self, symbol: str) -> Quote:
        logger.info(f"Fetching quote for {symbol} using DuckDuckGo fallback")
        query = f"{symbol} stock price"
        
        try:
            with DDGS() as ddgs:
                # Try the answers endpoint first which often returns instant answers
                answers = list(ddgs.answers(query))
                if answers:
                    for answer in answers:
                        text = answer.get("text", "")
                        price = self._extract_price(text)
                        if price:
                            return Quote(
                                symbol=symbol,
                                price=float(price),
                                currency="USD",  # Defaulting, as extraction is unreliable
                                source="duckduckgo"
                            )
                
                # Fallback to standard text search snippets
                results = list(ddgs.text(query, max_results=3))
                for result in results:
                    snippet = result.get("body", "")
                    price = self._extract_price(snippet)
                    if price:
                        return Quote(
                            symbol=symbol,
                            price=float(price),
                            currency="USD",
                            source="duckduckgo"
                        )
            
            raise ProviderUnavailableError(f"Could not extract price for {symbol} from DuckDuckGo")
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed for {symbol}: {e}")
            raise ProviderUnavailableError(f"DuckDuckGo search failed: {e}")

    def _extract_price(self, text: str) -> Decimal | None:
        """
        Attempt to extract a stock price from unstructured text.
        Looks for patterns like '150.25' near keywords.
        """
        # Very basic heuristic: look for currency symbols or words indicating price
        # This regex looks for an optional $ or INR, followed by numbers and decimals
        matches = re.findall(r'(?:[₹$]|USD|INR)?\s*(\d+(?:,\d{3})*(?:\.\d{1,2})?)', text)
        for match in matches:
            try:
                # Clean up commas
                clean_num = match.replace(',', '')
                return Decimal(clean_num)
            except Exception:
                continue
        return None

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        logger.warning(f"DuckDuckGoProvider cannot fetch historical prices for {symbol}")
        raise ProviderUnavailableError("Historical prices not supported by DuckDuckGo fallback")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        logger.warning(f"DuckDuckGoProvider cannot fetch company profile for {symbol}")
        raise ProviderUnavailableError("Company profile not supported by DuckDuckGo fallback")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        logger.warning(f"DuckDuckGoProvider cannot fetch financial metrics for {symbol}")
        raise ProviderUnavailableError("Financial metrics not supported by DuckDuckGo fallback")
