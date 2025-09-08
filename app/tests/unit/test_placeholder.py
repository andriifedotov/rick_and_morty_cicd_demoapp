import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCharactersAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_characters_list_ok(self):
        """GET /characters/ should return 200 OK and JSON"""
        response = self.client.get("/characters/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_character_not_found(self):
        """GET /characters/999999 should return 404"""
        response = self.client.get("/characters/999999/")
        assert response.status_code == 404

    def test_invalid_method(self):
        """POST /characters/ should return 405 (method not allowed)"""
        response = self.client.post("/characters/", data={"name": "Morty"})
        assert response.status_code == 405
