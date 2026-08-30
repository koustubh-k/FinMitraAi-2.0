from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import repositories
from app.financial import engine, errors
from app.models.holding import Holding
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction, TransactionType
from app.schemas.financial import (
    AllocationResponse,
    PortfolioSummary,
    PositionAllocation,
    PositionSummary,
    TransactionCreate,
)
from app.schemas.portfolio import PortfolioCreate
from app.services.market_data import MarketDataService


class PortfolioService:
    def __init__(self, db: Session):
        self.db = db

    def _get_portfolio_owned_by_user(self, user_id: UUID, portfolio_id: UUID) -> Portfolio:
        portfolio = self.db.query(Portfolio).filter(
            Portfolio.id == portfolio_id, Portfolio.user_id == user_id
        ).first()
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
        return portfolio

    def get_user_portfolios(self, user_id: UUID, skip: int = 0, limit: int = 100) -> list[Portfolio]:
        return repositories.portfolio.get_by_user_id(self.db, user_id=user_id, skip=skip, limit=limit)

    def create_portfolio(self, user_id: UUID, portfolio_in: PortfolioCreate) -> Portfolio:
        existing_portfolio = repositories.portfolio.get_by_user_and_name(
            self.db, user_id=user_id, name=portfolio_in.name
        )
        if existing_portfolio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A portfolio with this name already exists for this user.",
            )
        
        obj_in_data = portfolio_in.model_dump()
        obj_in_data["user_id"] = user_id
        
        db_obj = Portfolio(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_transactions(self, user_id: UUID, portfolio_id: UUID, skip: int = 0, limit: int = 100) -> list[Transaction]:
        self._get_portfolio_owned_by_user(user_id, portfolio_id)
        
        return self.db.query(Transaction).filter(
            Transaction.portfolio_id == portfolio_id
        ).order_by(desc(Transaction.transaction_date), desc(Transaction.created_at)).offset(skip).limit(limit).all()

    def get_holdings(self, user_id: UUID, portfolio_id: UUID) -> list[Holding]:
        self._get_portfolio_owned_by_user(user_id, portfolio_id)
        
        return self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id,
            Holding.quantity > 0
        ).all()

    def add_transaction(self, user_id: UUID, portfolio_id: UUID, transaction_in: TransactionCreate) -> Transaction:
        self._get_portfolio_owned_by_user(user_id, portfolio_id)
        
        symbol = transaction_in.symbol.upper()
        
        try:
            with self.db.begin_nested():
                # Lock the holding row to prevent concurrent modification races
                holding = self.db.query(Holding).filter(
                    Holding.portfolio_id == portfolio_id, 
                    Holding.symbol == symbol
                ).with_for_update().first()
                
                if not holding:
                    holding = Holding(
                        portfolio_id=portfolio_id,
                        symbol=symbol,
                        quantity=Decimal(0),
                        average_cost=Decimal(0)
                    )
                    self.db.add(holding)
                    # flush to get holding object locked conceptually
                    self.db.flush()
                
                if transaction_in.transaction_type == TransactionType.BUY:
                    new_avg_cost = engine.calculate_average_cost(
                        current_quantity=holding.quantity,
                        current_average_cost=holding.average_cost,
                        buy_quantity=transaction_in.quantity,
                        buy_price=transaction_in.price
                    )
                    holding.quantity += transaction_in.quantity
                    holding.average_cost = new_avg_cost
                    
                elif transaction_in.transaction_type == TransactionType.SELL:
                    if transaction_in.quantity > holding.quantity:
                        raise errors.InsufficientPositionError(f"Cannot sell {transaction_in.quantity} shares. Only {holding.quantity} held.")
                    
                    holding.quantity -= transaction_in.quantity
                    
                    if holding.quantity == Decimal(0):
                        holding.average_cost = Decimal(0)
                        
                else:
                    raise errors.UnsupportedTransactionTypeError(f"Unsupported transaction type: {transaction_in.transaction_type}")

                new_transaction = Transaction(
                    portfolio_id=portfolio_id,
                    symbol=symbol,
                    transaction_type=transaction_in.transaction_type,
                    quantity=transaction_in.quantity,
                    price=transaction_in.price,
                    transaction_date=transaction_in.transaction_date
                )
                self.db.add(new_transaction)

            self.db.commit()
            self.db.refresh(new_transaction)
            return new_transaction
            
        except errors.FinancialDomainError as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception:
            self.db.rollback()
            raise

    def get_portfolio_summary(self, user_id: UUID, portfolio_id: UUID, market_data_service: MarketDataService) -> PortfolioSummary:
        self._get_portfolio_owned_by_user(user_id, portfolio_id)
        
        holdings = self.get_holdings(user_id, portfolio_id)
        
        # Calculate invested capital from transactions (simplistic definition)
        transactions = self.db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).all()
        
        # In a more robust system, total realized P&L is tracked historically.
        # Since Phase 3 asks to calculate portfolio-level realized PNL from transactions, we must sum it up.
        total_portfolio_realized_pnl = Decimal(0)
        
        # We need a rolling average cost tracker if we are doing this strictly from transactions,
        # but for Phase 3, we can derive cumulative realized PNL by simulating the history per symbol.
        symbol_avg_cost = {}
        symbol_qty = {}
        
        for t in sorted(transactions, key=lambda x: (x.transaction_date, x.created_at)):
            sym = t.symbol
            if sym not in symbol_avg_cost:
                symbol_avg_cost[sym] = Decimal(0)
                symbol_qty[sym] = Decimal(0)
                
            if t.transaction_type == TransactionType.BUY:
                symbol_avg_cost[sym] = engine.calculate_average_cost(
                    symbol_qty[sym], symbol_avg_cost[sym], t.quantity, t.price
                )
                symbol_qty[sym] += t.quantity
            elif t.transaction_type == TransactionType.SELL:
                pnl = engine.calculate_realized_pnl(t.quantity, t.price, symbol_avg_cost[sym])
                total_portfolio_realized_pnl += pnl
                symbol_qty[sym] -= t.quantity
                if symbol_qty[sym] == Decimal(0):
                    symbol_avg_cost[sym] = Decimal(0)

        # Now compute current positions
        position_summaries = []
        portfolio_market_value = Decimal(0)
        portfolio_cost_basis = Decimal(0)
        portfolio_unrealized_pnl = Decimal(0)
        
        all_prices_available = True
        
        for holding in holdings:
            symbol = holding.symbol
            try:
                # Get quote
                quote = market_data_service.get_quote(symbol)
                market_price = Decimal(str(quote.price)) if quote and quote.price is not None else None
            except Exception:
                market_price = None

            cost_basis = engine.calculate_cost_basis(holding.quantity, holding.average_cost)
            market_value = engine.calculate_market_value(holding.quantity, market_price)
            unrealized_pnl = engine.calculate_unrealized_pnl(market_value, cost_basis)
            
            # Since holding table does not store per-symbol total realized P&L across history, 
            # we don't have per-symbol cumulative realized P&L in the holding table. 
            # We'd have to calculate it. Let's compute per-symbol realized PNL from transactions.
            symbol_realized_pnl = Decimal(0)
            s_avg_cost = Decimal(0)
            s_qty = Decimal(0)
            for t in sorted([t for t in transactions if t.symbol == symbol], key=lambda x: (x.transaction_date, x.created_at)):
                if t.transaction_type == TransactionType.BUY:
                    s_avg_cost = engine.calculate_average_cost(s_qty, s_avg_cost, t.quantity, t.price)
                    s_qty += t.quantity
                elif t.transaction_type == TransactionType.SELL:
                    symbol_realized_pnl += engine.calculate_realized_pnl(t.quantity, t.price, s_avg_cost)
                    s_qty -= t.quantity
                    if s_qty == Decimal(0):
                        s_avg_cost = Decimal(0)
            
            total_pnl = engine.calculate_total_pnl(symbol_realized_pnl, unrealized_pnl)
            
            valuation_status = "AVAILABLE" if market_price is not None else "UNAVAILABLE"
            
            pos = PositionSummary(
                symbol=symbol,
                quantity=holding.quantity,
                average_cost=holding.average_cost,
                cost_basis=cost_basis,
                market_price=market_price,
                market_value=market_value,
                realized_pnl=symbol_realized_pnl,
                unrealized_pnl=unrealized_pnl,
                total_pnl=total_pnl,
                valuation_status=valuation_status
            )
            position_summaries.append(pos)
            
            portfolio_cost_basis += cost_basis
            if market_value is not None:
                portfolio_market_value += market_value
                portfolio_unrealized_pnl += unrealized_pnl
            else:
                all_prices_available = False

        if not all_prices_available:
            portfolio_market_value = None
            portfolio_unrealized_pnl = None
            portfolio_total_pnl = None
            return_percentage = None
        else:
            portfolio_total_pnl = engine.calculate_total_pnl(total_portfolio_realized_pnl, portfolio_unrealized_pnl)
            return_percentage = engine.calculate_return_percentage(portfolio_total_pnl, portfolio_cost_basis)
        
        return PortfolioSummary(
            portfolio_id=portfolio_id,
            market_value=portfolio_market_value,
            cost_basis=portfolio_cost_basis,
            realized_pnl=total_portfolio_realized_pnl,
            unrealized_pnl=portfolio_unrealized_pnl,
            total_pnl=portfolio_total_pnl,
            return_percentage=return_percentage,
            positions=position_summaries
        )

    def get_allocation(self, user_id: UUID, portfolio_id: UUID, market_data_service: MarketDataService) -> AllocationResponse:
        summary = self.get_portfolio_summary(user_id, portfolio_id, market_data_service)
        
        allocations = []
        for pos in summary.positions:
            weight = engine.calculate_allocation(pos.market_value, summary.market_value)
            allocations.append(
                PositionAllocation(
                    symbol=pos.symbol,
                    market_value=pos.market_value,
                    weight_percentage=weight,
                    valuation_status=pos.valuation_status
                )
            )
            
        return AllocationResponse(positions=allocations)

