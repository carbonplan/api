import pytest
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    expected = {
        "projects_url": "https://api.carbonplan.org/projects",
        "schema_url": "https://api.carbonplan.org/schema",
    }
    assert response.json() == expected


@pytest.mark.parametrize("endpoint", ["projects", "schema"])
def test_endpoints(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json()


def test_project_query_arg():
    response = client.get("projects?id=STRP05")
    assert response.status_code == 200
    assert response.json()


def test_project_bad_query_arg_returns_empty():
    response = client.get("projects?id=NOTAPROJECT")
    assert response.status_code == 200
    assert response.json() == {}
