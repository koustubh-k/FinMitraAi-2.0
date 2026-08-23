from typing import Dict, Type
from app.providers.market.base import MarketDataProvider
from app.providers.market.mock import MockMarketDataProvider
from app.providers.market.yahoo import YahooProvider

class ProviderRegistry:
    """Registry for managing market data providers."""
    
    def __init__(self):
        self._providers: Dict[str, MarketDataProvider] = {
            "mock": MockMarketDataProvider(),
            "yahoo": YahooProvider()
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
