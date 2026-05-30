import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from main import app
from database import get_db

SAMPLE_RANKINGS = [
    {"rank": 1, "points": 9000.0, "name_first": "Novak", "name_last": "Djokovic", "country": "SRB", "height": 188.0},
    {"rank": 2, "points": 8500.0, "name_first": "Carlos", "name_last": "Alcaraz", "country": "ESP", "height": 185.0},
    {"rank": 3, "points": 7000.0, "name_first": "Jannik", "name_last": "Sinner", "country": "ITA", "height": 188.0},
    {"rank": 4, "points": 6500.0, "name_first": "Daniil", "name_last": "Medvedev", "country": "RUS", "height": 198.0},
    {"rank": 5, "points": 5000.0, "name_first": "Alexander", "name_last": "Zverev", "country": "GER", "height": 198.0},
]

SAMPLE_PLAYERS = [
    {"player_id": 100644, "name_first": "Roger", "name_last": "Federer", "country": "SUI", "height": 185.0},
]


@pytest.fixture
def client():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def error_client():
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


class TestTopRankings:
    def test_returns_top_5_players(self, client):
        with patch("router.get_top_players", return_value=SAMPLE_RANKINGS):
            response = client.get("/api/rankings/top")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert data[0]["rank"] == 1
        assert data[0]["name"] == "Novak Djokovic"

    def test_service_error_returns_500(self, error_client):
        with patch("router.get_top_players", side_effect=Exception("DB unavailable")):
            response = error_client.get("/api/rankings/top")

        assert response.status_code == 500

    def test_security_headers_present(self, client):
        with patch("router.get_top_players", return_value=SAMPLE_RANKINGS):
            response = client.get("/api/rankings/top")

        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert "Content-Security-Policy" in response.headers


class TestPlayerSearch:
    def test_returns_matching_players(self, client):
        with patch("router.find_players", return_value=SAMPLE_PLAYERS):
            response = client.get("/api/players/search?q=federer")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Roger Federer"
        assert data[0]["country"] == "SUI"

    def test_query_too_short_returns_422(self, client):
        response = client.get("/api/players/search?q=x")

        assert response.status_code == 422

    def test_no_results_returns_empty_list(self, client):
        with patch("router.find_players", return_value=[]):
            response = client.get("/api/players/search?q=zzzzzzzz")

        assert response.status_code == 200
        assert response.json() == []
