from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_screener_default():

    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_screener_min_roe():

    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200

    companies = response.json()

    for company in companies:

        assert company["return_on_equity_pct"] >= 15


def test_screener_max_de():

    response = client.get("/api/v1/screener?max_de=1")

    assert response.status_code == 200

    companies = response.json()

    for company in companies:

        assert company["debt_to_equity"] <= 1


def test_screener_max_pe():

    response = client.get("/api/v1/screener?max_pe=30")

    assert response.status_code == 200

    companies = response.json()

    for company in companies:

        assert company["pe_ratio"] <= 30


def test_screener_market_cap():

    response = client.get("/api/v1/screener?min_market_cap=1000")

    assert response.status_code == 200

    companies = response.json()

    for company in companies:

        assert company["market_cap_crore"] >= 1000


def test_invalid_parameter():

    response = client.get("/api/v1/screener?min_roe=abc")

    assert response.status_code == 422
