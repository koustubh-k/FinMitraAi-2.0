from decimal import Decimal


def calculate_average_cost(
    current_quantity: Decimal, 
    current_average_cost: Decimal, 
    buy_quantity: Decimal, 
    buy_price: Decimal
) -> Decimal:
    """
    Calculate the new weighted average cost after a BUY transaction.
    (current_qty * current_avg_cost + buy_qty * buy_price) / (current_qty + buy_qty)
    """
    if buy_quantity < 0:
        raise ValueError("Buy quantity cannot be negative")
    if buy_price < 0:
        raise ValueError("Buy price cannot be negative")
        
    total_current_cost = current_quantity * current_average_cost
    total_buy_cost = buy_quantity * buy_price
    
    new_quantity = current_quantity + buy_quantity
    if new_quantity == Decimal(0):
        return Decimal(0)
        
    return (total_current_cost + total_buy_cost) / new_quantity

def calculate_cost_basis(quantity: Decimal, average_cost: Decimal) -> Decimal:
    """
    Cost basis is the amount assigned to the currently held position.
    quantity * average_cost
    """
    return quantity * average_cost

def calculate_realized_pnl(
    sell_quantity: Decimal, 
    sell_price: Decimal, 
    average_cost: Decimal
) -> Decimal:
    """
    Realized P&L applies to sold shares.
    sale_proceeds - cost_basis_of_sold_shares
    """
    if sell_quantity < 0:
        raise ValueError("Sell quantity cannot be negative")
        
    sale_proceeds = sell_quantity * sell_price
    cost_basis_sold = sell_quantity * average_cost
    
    return sale_proceeds - cost_basis_sold

def calculate_market_value(quantity: Decimal, market_price: Decimal | None) -> Decimal | None:
    if market_price is None:
        return None
    return quantity * market_price

def calculate_unrealized_pnl(
    market_value: Decimal | None, 
    cost_basis: Decimal
) -> Decimal | None:
    """
    Unrealized P&L for shares still held.
    market_value - current_cost_basis
    """
    if market_value is None:
        return None
    return market_value - cost_basis

def calculate_total_pnl(
    realized_pnl: Decimal, 
    unrealized_pnl: Decimal | None
) -> Decimal | None:
    """
    Total P&L = realized P&L + unrealized P&L
    """
    if unrealized_pnl is None:
        return None
    return realized_pnl + unrealized_pnl

def calculate_return_percentage(
    total_pnl: Decimal | None, 
    invested_capital: Decimal
) -> Decimal | None:
    """
    Simple return: total_pnl / invested_capital * 100
    If invested capital is 0, return 0 or None.
    """
    if total_pnl is None:
        return None
    if invested_capital == Decimal(0):
        return Decimal(0)
    return (total_pnl / invested_capital) * Decimal(100)

def calculate_allocation(
    position_market_value: Decimal | None, 
    portfolio_market_value: Decimal | None
) -> Decimal | None:
    """
    allocation = position market value / total portfolio market value * 100
    """
    if position_market_value is None or portfolio_market_value is None:
        return None
    if portfolio_market_value == Decimal(0):
        return Decimal(0)
    return (position_market_value / portfolio_market_value) * Decimal(100)
