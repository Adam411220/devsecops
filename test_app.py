import sqlite3
import pytest
from app import app

@pytest.fixture(autouse=True)
def setup_db():
    """Tworzy tymczasową bazę z tabelą users przed każdym testem"""
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    conn.execute("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'testuser')")
    conn.commit()
    conn.close()
    yield

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
