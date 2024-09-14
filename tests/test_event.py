import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_event_deposit(client):
    response = client.post('/event', json={
        "type": "deposit",
        "amount": "50.00",
        "user_id": 1,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json['alert'] == False

# Add more tests for the different alert codes and edge cases
