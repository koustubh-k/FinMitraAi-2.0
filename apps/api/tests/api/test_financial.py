import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.main import app
from app.models.portfolio import Portfolio
from app.models.user import User
from app.services.market_data import MarketDataService

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_user(db_session: Session):
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email=f"test_fin_{user_id}@example.com",
        password_hash="dummy_hash",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="module")
def test_portfolio(db_session: Session, test_user: User):
    port = Portfolio(
        id=uuid.uuid4(),
        user_id=test_user.id,
        name="End to End Test Portfolio"
    )
    db_session.add(port)
    db_session.commit()
    db_session.refresh(port)
    return port

from app.services.market_data import get_market_data_service


@pytest.fixture(autouse=True)
def override_dependencies(db_session: Session, test_user: User):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: test_user
    
    # Force the mock provider for tests
    app.dependency_overrides[get_market_data_service] = lambda: MarketDataService("mock")
    
    yield
    app.dependency_overrides.clear()

def test_financial_end_to_end(db_session: Session, test_portfolio: Portfolio):
    portfolio_id = test_portfolio.id
    
    # 1. Create BUY 10 TCS
    tx1 = {
        "symbol": "TCS",
        "transaction_type": "BUY",
        "quantity": "10",
        "price": "3000",
        "transaction_date": datetime.now(timezone.utc).isoformat()
    }
    r = client.post(f"/api/v1/portfolios/{portfolio_id}/transactions", json=tx1)
    assert r.status_code == 201

    # 2. Create BUY 5 TCS
    tx2 = {
        "symbol": "TCS",
        "transaction_type": "BUY",
        "quantity": "5",
        "price": "3200",
        "transaction_date": datetime.now(timezone.utc).isoformat()
    }
    r = client.post(f"/api/v1/portfolios/{portfolio_id}/transactions", json=tx2)
    assert r.status_code == 201
    
    # 3. Create SELL 2 TCS
    tx3 = {
        "symbol": "TCS",
        "transaction_type": "SELL",
        "quantity": "2",
        "price": "3300",
        "transaction_date": datetime.now(timezone.utc).isoformat()
    }
    r = client.post(f"/api/v1/portfolios/{portfolio_id}/transactions", json=tx3)
    assert r.status_code == 201
    
    # 4. Check Holdings
    r_hold = client.get(f"/api/v1/portfolios/{portfolio_id}/holdings")
    assert r_hold.status_code == 200
    holdings = r_hold.json()
    assert len(holdings) == 1
    assert holdings[0]["symbol"] == "TCS"
    assert holdings[0]["quantity"] == "13.00000000"
    
    # 5. Check Summary
    r_sum = client.get(f"/api/v1/portfolios/{portfolio_id}/summary")
    assert r_sum.status_code == 200
    summary = r_sum.json()
    
    # Validation logic:
    # BUY 10 @ 3000, BUY 5 @ 3200 => Qty: 15, Cost: 46000, AvgCost: 3066.66666667
    # SELL 2 @ 3300 => Qty: 13, AvgCost: 3066.66666667
    # Cost Basis = 13 * 3066.66666667 = 39866.66666671
    # Realized PNL = 2 * (3300 - 3066.66666667) = 2 * 233.33333333 = 466.66666666
    assert float(summary["cost_basis"]) > 39866.0
    assert float(summary["cost_basis"]) < 39867.0
    
    # MockProvider always returns price = 100.0
    market_val = float(summary["market_value"])
    assert market_val == 1300.0 # 13 * 100.0
    
    real_pnl = float(summary["realized_pnl"])
    assert real_pnl > 466.0
    assert real_pnl < 467.0
    
    unreal_pnl = float(summary["unrealized_pnl"])
    # 1300.0 - 39866.6666 = -38566.6666
    assert unreal_pnl > -38567.0
    assert unreal_pnl < -38566.0
    
    tot_pnl = float(summary["total_pnl"])
    assert tot_pnl > -38101.0
    assert tot_pnl < -38100.0
    
    # 6. Check Allocation
    r_alloc = client.get(f"/api/v1/portfolios/{portfolio_id}/allocation")
    assert r_alloc.status_code == 200
    alloc = r_alloc.json()
    assert len(alloc["positions"]) == 1
    assert float(alloc["positions"][0]["weight_percentage"]) == 100.0

