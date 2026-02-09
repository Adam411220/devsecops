import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_debug_route(client):
    """Sprawdza czy strona debug działa"""
    res = client.get('/debug')
    assert res.status_code == 200

def test_user_route(client):
    """Sprawdza czy strona user odpowiada"""
    res = client.get('/user?id=1')
    assert res.status_code == 200