import io

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    expected = {
        "projects_url": "https://api.carbonplan.org/projects.json",
        "schema_url": "https://api.carbonplan.org/schema.json",
        "docs_url": "https://api.carbonplan.org/docs",
    }
    assert response.json() == expected


@pytest.mark.parametrize(
    "endpoint", ["projects.json", "schema.json", "v0/projects.json", "v0/schema.json"]
)
def test_endpoints(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    assert response.json()
    assert response.headers["content-type"] == "application/json; charset=utf-8"


@pytest.mark.parametrize("endpoint", ["projects.csv", "v0/projects.csv"])
def test_endpoints_csv(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    str_data = io.StringIO(response.content.decode())
    assert len(pd.read_csv(str_data))
    assert response.headers["content-type"] == "text/csv; charset=utf-8"


def test_project_query_arg():
    response = client.get("projects.json?id=STRP05")
    assert response.status_code == 200
    assert response.json()
    assert response.headers["content-type"] == "application/json; charset=utf-8"


def test_project_bad_query_arg_returns_empty():
    response = client.get("projects.json?id=NOTAPROJECT")
    assert response.status_code == 200
    assert response.json() == {}
    assert response.headers["content-type"] == "application/json; charset=utf-8"


def test_docs_render():
    response = client.get("docs")
    assert response.status_code == 200
