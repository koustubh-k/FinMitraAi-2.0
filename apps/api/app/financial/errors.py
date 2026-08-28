class FinancialDomainError(Exception):
    """Base exception for financial domain errors."""

class InsufficientPositionError(FinancialDomainError):
    """Raised when attempting to sell more shares than currently held."""

class InvalidTransactionError(FinancialDomainError):
    """Raised when transaction data is invalid for the financial context."""

class UnsupportedTransactionTypeError(FinancialDomainError):
    """Raised for unsupported transaction types."""

class MarketPriceUnavailableError(FinancialDomainError):
    """Raised when market price is explicitly required but unavailable."""
