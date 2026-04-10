from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_status_api():
    response = client.get("/status")
    assert response.status_code == 200
    assert "status" in response.json()


def test_login_fail():
    response = client.post(
        "/token",
        data={"username": "admin@replantio.com", "password": "1234567890"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "E-mail ou palavra-passe incorretos"}


def test_route_access_without_token():
    response = client.get("/mudas/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
