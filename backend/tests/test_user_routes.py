import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from digital_twin import app
from datetime import date

client = TestClient(app)

@pytest.fixture
def mock_db():
    return MagicMock()


def test_register_user_success(mock_db):
    """Testa criação bem-sucedida de um user."""

    mock_user = MagicMock(
        id=1,
        name="Guilherme Gonçalves",
        birthdate="2001-01-01",
        email="ggoncalves@gmail.com",
        password="Password2025"
    )

    with patch("digital_twin.services.user.UserService.add_user", return_value=mock_user):

        payload = {
            "name": "Guilherme Gonçalves",
            "birthdate": "2001-01-01",
            "email": "ggoncalves@gmail.com",
            "password": "Password2025"
        }

        response = client.post("/api/v1/users/register", json=payload)

        assert response.status_code == 204


def test_register_user_email_exists(mock_db):
    """Testa criação de um user com email que já existe."""

    with patch("digital_twin.services.user.UserService.add_user", return_value=None):

        payload = {
            "name": "Guilherme Gonçalves",
            "birthdate": "2001-01-01",
            "email": "ggoncalves@gmail.com",
            "password": "Password2025"
        }

        response = client.post("/api/v1/users/register", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Email already in use. Try another one."


def test_login_user_success(mock_db):
    """Testa autenticação bem sucedida de um user."""

    mock_user = MagicMock(
        id=1,
        name="Guilherme Gonçalves",
        birthdate="2001-01-01",
        email="ggoncalves@gmail.com",
        password="Password2025"
    )

    with patch("digital_twin.services.user.UserService.authenticate_user", return_value=mock_user), \
        patch("digital_twin.routers.users.create_access_token", return_value="fake-jwt-token-123"):

        payload = {
            "email": "ggoncalves@gmail.com",
            "password": "Password2025"
        }

        response = client.post("/api/v1/users/login", json=payload)

        assert response.status_code == 200
        assert response.json()["access_token"] == "fake-jwt-token-123"
        assert response.json()["token_type"] == "bearer"


def test_login_user_error(mock_db):
    """Testa autenticação incorreta de um user."""

    with patch("digital_twin.services.user.UserService.authenticate_user", return_value=False):

        payload = {
            "email": "fake-email@gmail.com",
            "password": "Password2025"
        }

        response = client.post("/api/v1/users/login", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Credentials invalid. Try again."
