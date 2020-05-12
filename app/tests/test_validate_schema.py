import jsonschema
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_validate_schema():
    schema = client.get("schema/ProjectCollection.json").json()
    assert schema
    project_collection = client.get("/projects.json").json()
    assert project_collection

    jsonschema.validate(project_collection, schema=schema)
