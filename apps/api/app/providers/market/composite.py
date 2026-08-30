from app.core.logger import setup_logger
from datetime import date

from app.core.errors import ProviderUnavailableError, SymbolNotFoundError
from app.providers.market.base import MarketDataProvider
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPriceResponse,
    Quote,
)

logger = setup_logger(__name__)


class CompositeMarketDataProvider(MarketDataProvider):
    """
    A market data provider that delegates to a list of fallback providers.
    It attempts each provider in order. If a provider fails with a generic error
    or ProviderUnavailableError, it tries the next one.
    If it raises SymbolNotFoundError, it stops and propagates it (since the symbol is invalid).
    """
    
    def __init__(self, providers: list[MarketDataProvider]):
        if not providers:
            raise ValueError("At least one provider must be specified for CompositeMarketDataProvider")
        self.providers = providers

    def get_quote(self, symbol: str) -> Quote:
        for provider in self.providers:
            try:
                logger.info(f"Attempting get_quote for {symbol} using {provider.__class__.__name__}")
                return provider.get_quote(symbol)
            except SymbolNotFoundError:
                raise
            except Exception as e:
                logger.warning(f"Provider {provider.__class__.__name__} failed for get_quote({symbol}): {e}")
                continue
        
        raise ProviderUnavailableError(f"All providers failed to fetch quote for {symbol}")

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        for provider in self.providers:
            try:
                logger.info(f"Attempting get_historical_prices for {symbol} using {provider.__class__.__name__}")
                return provider.get_historical_prices(symbol, start, end, interval)
            except SymbolNotFoundError:
                raise
            except Exception as e:
                logger.warning(f"Provider {provider.__class__.__name__} failed for get_historical_prices({symbol}): {e}")
                continue
        
        raise ProviderUnavailableError(f"All providers failed to fetch historical prices for {symbol}")

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        for provider in self.providers:
            try:
                logger.info(f"Attempting get_company_profile for {symbol} using {provider.__class__.__name__}")
                return provider.get_company_profile(symbol)
            except SymbolNotFoundError:
                raise
            except Exception as e:
                logger.warning(f"Provider {provider.__class__.__name__} failed for get_company_profile({symbol}): {e}")
                continue
        
        raise ProviderUnavailableError(f"All providers failed to fetch company profile for {symbol}")

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        for provider in self.providers:
            try:
                logger.info(f"Attempting get_financial_metrics for {symbol} using {provider.__class__.__name__}")
                return provider.get_financial_metrics(symbol)
            except SymbolNotFoundError:
                raise
            except Exception as e:
                logger.warning(f"Provider {provider.__class__.__name__} failed for get_financial_metrics({symbol}): {e}")
                continue
        
        raise ProviderUnavailableError(f"All providers failed to fetch financial metrics for {symbol}")
