import logging
from datetime import date

from app.core.config import settings
from app.core.errors import ProviderUnavailableError
from app.providers.market.base import MarketDataProvider
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)

logger = logging.getLogger(__name__)

class StubBaseProvider(MarketDataProvider):
    """Base class for stubbed providers."""
    
    @property
    def provider_name(self) -> str:
        return self.__class__.__name__.replace("Provider", "").lower()
        
    def get_quote(self, symbol: str) -> Quote:
        raise ProviderUnavailableError(f"{self.provider_name} provider is not fully implemented.")

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        raise ProviderUnavailableError(f"{self.provider_name} provider is not fully implemented.")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        raise ProviderUnavailableError(f"{self.provider_name} provider is not fully implemented.")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        raise ProviderUnavailableError(f"{self.provider_name} provider is not fully implemented.")


class MarketauxProvider(StubBaseProvider):
    def __init__(self):
        self.api_key = settings.marketaux_api_key

class ExaProvider(StubBaseProvider):
    def __init__(self):
        self.api_key = settings.exa_api_key

class FirecrawlProvider(StubBaseProvider):
    def __init__(self):
        self.api_key = settings.firecrawl_api_key
        
class SerperProvider(StubBaseProvider):
    def __init__(self):
        self.api_key = settings.serper_api_key

class LinkupProvider(StubBaseProvider):
    def __init__(self):
        self.api_key = settings.linkup_api_key

class SearXNGProvider(StubBaseProvider):
    def __init__(self):
        pass
