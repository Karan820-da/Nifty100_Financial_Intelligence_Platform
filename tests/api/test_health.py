from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_status():

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_health_contains_db_row_counts():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "db_row_counts" in data


def test_health_contains_all_tables():

    response = client.get("/api/v1/health")

    tables = response.json()["db_row_counts"]

    expected_tables = [
        "analysis",
        "balancesheet",
        "cashflow",
        "companies",
        "documents",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "peer_percentiles",
        "profitandloss",
        "prosandcons",
        "sectors",
        "stock_prices",
    ]

    for table in expected_tables:

        assert table in tables


def test_health_version_exists():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "version" in data


def test_health_uptime_exists():

    response = client.get("/api/v1/health")

    data = response.json()

    assert "uptime_seconds" in data
