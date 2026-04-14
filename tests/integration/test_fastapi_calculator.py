# tests/integration/test_fastapi_calculator.py

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """TestClient fixture for the FastAPI app."""
    with TestClient(app) as client:
        yield client


def test_add_api(client):
    response = client.post('/add', json={'a': 10, 'b': 5})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()['result'] == 15, f"Expected 15, got {response.json()['result']}"


def test_subtract_api(client):
    response = client.post('/subtract', json={'a': 10, 'b': 5})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()['result'] == 5, f"Expected 5, got {response.json()['result']}"


def test_multiply_api(client):
    response = client.post('/multiply', json={'a': 10, 'b': 5})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()['result'] == 50, f"Expected 50, got {response.json()['result']}"


def test_divide_api(client):
    response = client.post('/divide', json={'a': 10, 'b': 2})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()['result'] == 5, f"Expected 5, got {response.json()['result']}"


def test_divide_by_zero_api(client):
    response = client.post('/divide', json={'a': 10, 'b': 0})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON missing 'error' field"
    assert "Cannot divide by zero!" in response.json()['error']
