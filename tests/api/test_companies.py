from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_all_companies():

    response = client.get("/api/v1/companies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    # Your sprint expects 92 companies
    assert len(data) == 92


def test_get_company_tcs():

    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"

    assert "company_name" in data

    assert "latest_ratios" in data


def test_invalid_company():

    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Company not found"
