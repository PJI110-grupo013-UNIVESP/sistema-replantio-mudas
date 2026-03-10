# backend/app/tests/test_main.py
import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient   # noqa: E402
from app.main import app                    # noqa: E402


client = TestClient(app)


def test_access_blocked_without_token():

    response = client.get("/mudas")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_login_user_inexistente():

    response = client.post(
        "/token",
        data={"username": "hacker@email.com", "password": "123456"}
    )

    assert response.status_code == 401
