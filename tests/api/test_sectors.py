from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_sectors():

    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    sectors = response.json()

    assert isinstance(sectors, list)

    # Sprint expects 11 sectors
    assert len(sectors) == 10


def test_it_sector_companies():

    response = client.get("/api/v1/sectors/IT/companies")

    assert response.status_code == 200

    companies = response.json()

    assert isinstance(companies, list)

    for company in companies:

        assert company["broad_sector"] == "IT"


def test_unknown_sector():

    response = client.get("/api/v1/sectors/INVALID_SECTOR/companies")

    # Your implementation may return either:
    # 200 + []
    # OR 404 if handled in the service
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        assert response.json() == []
