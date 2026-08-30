from decimal import Decimal

import pytest

from app.financial import engine


def test_calculate_average_cost_initial_buy():
    # Initial buy 10 shares @ 100
    avg_cost = engine.calculate_average_cost(
        current_quantity=Decimal(0),
        current_average_cost=Decimal(0),
        buy_quantity=Decimal(10),
        buy_price=Decimal(100)
    )
    assert avg_cost == Decimal(100)

def test_calculate_average_cost_multiple_buys():
    # Buy 10 @ 100, then 5 @ 120
    avg_cost = engine.calculate_average_cost(
        current_quantity=Decimal(10),
        current_average_cost=Decimal(100),
        buy_quantity=Decimal(5),
        buy_price=Decimal(120)
    )
    # (1000 + 600) / 15 = 1600 / 15 = 106.666...
    assert round(avg_cost, 8) == round(Decimal(1600) / Decimal(15), 8)

def test_calculate_cost_basis():
    basis = engine.calculate_cost_basis(Decimal(15), Decimal("106.66666667"))
    assert round(basis, 2) == Decimal("1600.00")

def test_calculate_realized_pnl():
    # Sell 5 @ 130, avg cost 106.66666667
    pnl = engine.calculate_realized_pnl(Decimal(5), Decimal(130), Decimal("106.66666667"))
    # proceeds = 650, cost = 533.33333335
    assert round(pnl, 2) == Decimal("116.67")

def test_calculate_unrealized_pnl():
    # 10 shares held, market price 120
    market_value = engine.calculate_market_value(Decimal(10), Decimal(120))
    cost_basis = engine.calculate_cost_basis(Decimal(10), Decimal(100))
    unrealized = engine.calculate_unrealized_pnl(market_value, cost_basis)
    
    assert market_value == Decimal(1200)
    assert unrealized == Decimal(200)

def test_calculate_total_pnl():
    total = engine.calculate_total_pnl(Decimal(150), Decimal(200))
    assert total == Decimal(350)

def test_calculate_return_percentage():
    ret = engine.calculate_return_percentage(Decimal(1500), Decimal(10000))
    assert ret == Decimal(15)

def test_calculate_allocation():
    alloc = engine.calculate_allocation(Decimal(12000), Decimal(20000))
    assert alloc == Decimal(60)

def test_missing_market_price():
    market_value = engine.calculate_market_value(Decimal(10), None)
    assert market_value is None
    
    unrealized = engine.calculate_unrealized_pnl(market_value, Decimal(1000))
    assert unrealized is None
    
    total = engine.calculate_total_pnl(Decimal(100), unrealized)
    assert total is None

def test_negative_quantity_raises_error():
    with pytest.raises(ValueError):
        engine.calculate_average_cost(Decimal(10), Decimal(10), Decimal(-1), Decimal(10))
    with pytest.raises(ValueError):
        engine.calculate_realized_pnl(Decimal(-5), Decimal(10), Decimal(10))
