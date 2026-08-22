class MarketDataError(Exception):
    """Base class for market data exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ProviderUnavailableError(MarketDataError):
    """Raised when a market data provider is unavailable or down."""
    pass

class SymbolNotFoundError(MarketDataError):
    """Raised when a requested symbol is not found by the provider."""
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__(f"Symbol not found: {symbol}")

class RateLimitError(MarketDataError):
    """Raised when the provider's rate limit is exceeded."""
    pass

class InvalidMarketDataError(MarketDataError):
    """Raised when the provider returns malformed or invalid data."""
    pass
