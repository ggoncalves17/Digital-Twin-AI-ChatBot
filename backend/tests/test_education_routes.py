import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from digital_twin import app
from datetime import date

client = TestClient(app)

@pytest.fixture
def mock_db():
    """Mock da sessão da BD."""
    return MagicMock()


def test_create_education_success(mock_db):
    """Testa criação bem-sucedida de uma educação."""
    mock_education = MagicMock(
        id=1,
        persona_id=10,
        level="Master",
        course="Engenharia Informática",
        school="ISEC",
        date_started=date(2022, 9, 1),
        date_finished=None,
        is_graduated=False
    )

    with patch("digital_twin.services.education.EducationService.create_education", return_value=mock_education), \
         patch("digital_twin.routers.educations.export_data") as mock_export:

        payload = {
            "level": "Master",
            "course": "Engenharia Informática",
            "school": "ISEC",
            "date_started": date(2022, 9, 1).isoformat(),
            "is_graduated": False,
            "persona_id": 10
        }

        response = client.post("/api/v1/educations/", json=payload)

        assert response.status_code == 200
        assert response.json()["id"] == 1
        mock_export.assert_called()


def test_create_education_persona_not_found(mock_db):
    """Testa erro ao criar educação com persona inexistente."""
    with patch("digital_twin.services.education.EducationService.create_education", return_value=None), \
         patch("digital_twin.routers.educations.export_data") as mock_export:

        payload = {
            "level": "Master",
            "course": "Engenharia Informática",
            "school": "ISEC",
            "date_started": date(2022, 9, 1).isoformat(),
            "is_graduated": False,
            "persona_id": 999
        }

        response = client.post("/api/v1/educations/", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Persona id not found"
        mock_export.assert_called()


def test_get_education_success(mock_db):
    """Testa leitura de educação existente."""
    mock_education = MagicMock(
        id=1,
        persona_id=10,
        level="Master",
        course="Engenharia Informática",
        school="ISEC",
        date_started=date(2022, 9, 1),
        date_finished=None,
        is_graduated=False
    )

    with patch("digital_twin.services.education.EducationService.get_education", return_value=mock_education), \
         patch("digital_twin.utils.lakehouse_export.export_data"):
        response = client.get("/api/v1/educations/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1


def test_get_education_not_found(mock_db):
    """Testa erro ao tentar ler uma educação inexistente."""
    with patch("digital_twin.services.education.EducationService.get_education", return_value=None), \
         patch("digital_twin.utils.lakehouse_export.export_data"):
        response = client.get("/api/v1/educations/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Education not found"


def test_delete_education_success(mock_db):
    """Testa remoção com sucesso."""
    with patch("digital_twin.services.education.EducationService.delete_education", return_value=True), \
         patch("digital_twin.utils.lakehouse_export.export_data"):
        response = client.delete("/api/v1/educations/1")
        assert response.status_code == 204


def test_delete_education_not_found(mock_db):
    """Testa erro ao remover educação inexistente."""
    with patch("digital_twin.services.education.EducationService.delete_education", return_value=False), \
         patch("digital_twin.utils.lakehouse_export.export_data"):
        response = client.delete("/api/v1/educations/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Education not found"
