from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ops_login_invalid():
    response = client.post("/ops/login", json={"email": "wrong@x.com", "password": "pass"})
    assert response.status_code == 400

def test_client_signup():
    response = client.post("/client/signup", json={"email": "client@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "verify_link" in response.json()
