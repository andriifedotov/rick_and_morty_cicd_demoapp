import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCharactersAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_characters_list_ok(self):
        response = self.client.get("/api/characters/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_character_not_found(self):
        """GET /characters/999999 should return 404"""
        response = self.client.get("/api/characters/999999/")
        assert response.status_code == 404

    def test_invalid_method(self):
        """POST /characters/ should return 405 (method not allowed)"""
        response = self.client.post("/api/characters/", data={"name": "Morty"})
        assert response.status_code == 405
