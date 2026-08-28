from app.providers.market.base import MarketDataProvider
from app.providers.market.duckduckgo import DuckDuckGoProvider
from app.providers.market.mock import MockMarketDataProvider
from app.providers.market.yahoo import YahooProvider
from app.providers.market.alphavantage import AlphaVantageProvider
from app.providers.market.finnhub import FinnhubProvider
from app.providers.market.fmp import FMPProvider
from app.providers.market.tavily import TavilyProvider
from app.providers.market.stubs import (
    MarketauxProvider,
    ExaProvider,
    FirecrawlProvider,
    SerperProvider,
    LinkupProvider,
    SearXNGProvider
)


class ProviderRegistry:
    """Registry for managing market data providers."""
    
    def __init__(self):
        self._providers: dict[str, MarketDataProvider] = {
            "mock": MockMarketDataProvider(),
            "yahoo": YahooProvider(),
            "duckduckgo": DuckDuckGoProvider(),
            "alphavantage": AlphaVantageProvider(),
            "finnhub": FinnhubProvider(),
            "fmp": FMPProvider(),
            "tavily": TavilyProvider(),
            "marketaux": MarketauxProvider(),
            "exa": ExaProvider(),
            "firecrawl": FirecrawlProvider(),
            "serper": SerperProvider(),
            "linkup": LinkupProvider(),
            "searxng": SearXNGProvider()
        }

    def register(self, name: str, provider: MarketDataProvider):
        """Register a new provider dynamically."""
        self._providers[name] = provider

    def get(self, name: str) -> MarketDataProvider:
        """Get a provider by name."""
        provider = self._providers.get(name)
        if not provider:
            raise ValueError(f"Market data provider '{name}' is not registered.")
        return provider

# Global registry instance
provider_registry = ProviderRegistry()
