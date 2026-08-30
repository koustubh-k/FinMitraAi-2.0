from datetime import date

from app.core.config import settings
from app.providers.market.registry import provider_registry
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)


from app.providers.market.composite import CompositeMarketDataProvider

class MarketDataService:
    def __init__(self, provider_name: str = None):
        self.provider_name = provider_name or settings.market_data_provider
        
        provider_names = [name.strip() for name in self.provider_name.split(",")]
        
        if len(provider_names) == 1:
            self.provider = provider_registry.get(provider_names[0])
        else:
            providers = [provider_registry.get(name) for name in provider_names]
            self.provider = CompositeMarketDataProvider(providers)

    def normalize_symbol(self, symbol: str) -> str:
        """
        Normalize the symbol.
        For Indian equities on Yahoo, we typically need a .NS suffix.
        """
        symbol = symbol.strip().upper()
        if self.provider_name == "yahoo" and "." not in symbol:
            # Default to NSE (.NS) for Indian stocks if no exchange is specified
            # A more sophisticated mapping could be used in the future
            return f"{symbol}.NS"
        return symbol

    def _denormalize_symbol(self, normalized_symbol: str, original_symbol: str) -> str:
        """
        Remove the provider-specific suffix to return the original symbol to the user.
        """
        return original_symbol.strip().upper()

    def get_quote(self, symbol: str) -> Quote:
        norm_symbol = self.normalize_symbol(symbol)
        quote = self.provider.get_quote(norm_symbol)
        quote.symbol = self._denormalize_symbol(quote.symbol, symbol)
        return quote

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        norm_symbol = self.normalize_symbol(symbol)
        history = self.provider.get_historical_prices(norm_symbol, start, end, interval)
        history.symbol = self._denormalize_symbol(history.symbol, symbol)
        return history

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        norm_symbol = self.normalize_symbol(symbol)
        profile = self.provider.get_company_profile(norm_symbol)
        profile.symbol = self._denormalize_symbol(profile.symbol, symbol)
        return profile

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        norm_symbol = self.normalize_symbol(symbol)
        metrics = self.provider.get_financial_metrics(norm_symbol)
        metrics.symbol = self._denormalize_symbol(metrics.symbol, symbol)
        return metrics

# Dependency
def get_market_data_service() -> MarketDataService:
    return MarketDataService()
