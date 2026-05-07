from fastapi.testclient import TestClient
from src.api.app import app


client = TestClient(app)
def test_create_form():
    response = client.post("/create-form")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "created": "true"}
