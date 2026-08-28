from datetime import date, datetime, timezone

import pandas as pd
import yfinance as yf

from app.core.errors import (
    InvalidMarketDataError,
    ProviderUnavailableError,
    SymbolNotFoundError,
)
from app.schemas.market_data import (
    CompanyProfile,
    FinancialMetrics,
    HistoricalPrice,
    HistoricalPriceResponse,
    Quote,
    utc_now,
)


class YahooProvider:
    """Market data provider implementation using yfinance."""

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        return yf.Ticker(symbol)

    def get_quote(self, symbol: str) -> Quote:
        try:
            ticker = self._get_ticker(symbol)
            info = ticker.fast_info
            
            # fast_info throws AttributeError if the symbol is not found or has no price
            try:
                price = info.last_price
                if price is None:
                    raise SymbolNotFoundError(symbol)
            except Exception:
                raise SymbolNotFoundError(symbol)

            previous_close = info.previous_close
            day_change = price - previous_close if previous_close else None
            day_change_percent = (day_change / previous_close * 100) if day_change and previous_close else None

            # `currency` might not be in fast_info, fallback to info dict if needed,
            # but fast_info has `currency` usually.
            currency = getattr(info, 'currency', 'USD')
            
            return Quote(
                symbol=symbol,
                price=price,
                currency=currency,
                timestamp=utc_now(), # Realtime timestamps vary, use current UTC as proxy for "now"
                previous_close=previous_close,
                day_change=day_change,
                day_change_percent=day_change_percent,
                data_timestamp=utc_now()
            )
        except SymbolNotFoundError:
            raise
        except Exception as e:
            if "Rate" in str(e): # generic fallback
                raise ProviderUnavailableError("Yahoo Finance provider is unavailable") from e
            raise InvalidMarketDataError(f"Failed to fetch quote for {symbol}: {e!s}") from e

    def get_historical_prices(self, symbol: str, start: date, end: date, interval: str) -> HistoricalPriceResponse:
        try:
            ticker = self._get_ticker(symbol)
            # yfinance expects date strings or datetime objects
            df = ticker.history(start=start.isoformat(), end=end.isoformat(), interval=interval)
            
            if df.empty:
                # Check if it's because of a missing symbol or just a weekend/holiday
                # We can do a quick info check to see if the symbol exists
                try:
                    _ = ticker.fast_info.last_price
                except Exception:
                    raise SymbolNotFoundError(symbol)
                # If symbol exists but df is empty, return empty list
                return HistoricalPriceResponse(
                    symbol=symbol,
                    interval=interval,
                    data=[]
                )
                
            data = []
            for ts, row in df.iterrows():
                # Make sure the timestamp is UTC
                if isinstance(ts, pd.Timestamp):
                    if ts.tzinfo is None:
                        dt = ts.replace(tzinfo=timezone.utc).to_pydatetime()
                    else:
                        dt = ts.astimezone(timezone.utc).to_pydatetime()
                else:
                    dt = datetime.combine(ts, datetime.min.time()).replace(tzinfo=timezone.utc)

                data.append(
                    HistoricalPrice(
                        timestamp=dt,
                        open=float(row['Open']),
                        high=float(row['High']),
                        low=float(row['Low']),
                        close=float(row['Close']),
                        adjusted_close=float(row.get('Adj Close', row['Close'])),
                        volume=int(row['Volume'])
                    )
                )

            return HistoricalPriceResponse(
                symbol=symbol,
                interval=interval,
                data=data
            )
        except SymbolNotFoundError:
            raise
        except Exception as e:
            raise InvalidMarketDataError(f"Failed to fetch historical prices for {symbol}: {e!s}") from e

    def get_company_profile(self, symbol: str) -> CompanyProfile:
        try:
            ticker = self._get_ticker(symbol)
            # The 'info' dict can take some time to fetch
            info = ticker.info
            
            if not info or 'shortName' not in info:
                raise SymbolNotFoundError(symbol)

            return CompanyProfile(
                symbol=symbol,
                name=info.get('shortName') or info.get('longName') or symbol,
                exchange=info.get('exchange'),
                currency=info.get('currency'),
                sector=info.get('sector'),
                industry=info.get('industry'),
                country=info.get('country'),
                data_timestamp=utc_now()
            )
        except SymbolNotFoundError:
            raise
        except Exception as e:
            raise InvalidMarketDataError(f"Failed to fetch profile for {symbol}: {e!s}") from e

    def get_financial_metrics(self, symbol: str) -> FinancialMetrics:
        try:
            ticker = self._get_ticker(symbol)
            info = ticker.info
            
            if not info or ('regularMarketPrice' not in info and 'previousClose' not in info):
                raise SymbolNotFoundError(symbol)

            return FinancialMetrics(
                symbol=symbol,
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE') or info.get('forwardPE'),
                eps=info.get('trailingEps') or info.get('forwardEps'),
                dividend_yield=info.get('dividendYield'),
                beta=info.get('beta'),
                data_timestamp=utc_now()
            )
        except SymbolNotFoundError:
            raise
        except Exception as e:
            raise InvalidMarketDataError(f"Failed to fetch metrics for {symbol}: {e!s}") from e
