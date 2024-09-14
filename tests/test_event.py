import pytest
from app import app


# This fixture provides a Flask test client for making requests to the app.
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test: Deposit without triggering any alert
def test_event_deposit_no_alert(client):
    response = client.post('/event', json={
        "type": "deposit",
        "amount": "50.00",
        "user_id": 1,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json['alert'] == False
    assert response.json['alert_codes'] == []
    assert response.json['user_id'] == 1


# Test: Withdrawal over 100 (Should trigger alert code 1100)
def test_event_withdrawal_over_100(client):
    response = client.post('/event', json={
        "type": "withdraw",
        "amount": "150.00",
        "user_id": 2,
        "time": 20
    })
    assert response.status_code == 200
    assert response.json['alert'] == True
    assert 1100 in response.json['alert_codes']
    assert response.json['user_id'] == 2


# Test: 3 Consecutive Withdrawals (Should trigger alert code 30)
def test_event_three_consecutive_withdrawals(client):
    client.post('/event', json={"type": "withdraw", "amount": "50.00", "user_id": 3, "time": 5})
    client.post('/event', json={"type": "withdraw", "amount": "30.00", "user_id": 3, "time": 10})
    response = client.post('/event', json={"type": "withdraw", "amount": "70.00", "user_id": 3, "time": 15})

    assert response.status_code == 200
    assert response.json['alert'] == True
    assert 30 in response.json['alert_codes']
    assert response.json['user_id'] == 3


# Test: Missing Fields (Should return 400 with an error message)
def test_event_missing_fields(client):
    response = client.post('/event', json={
        "amount": "50.00",  # Missing 'type' field
        "user_id": 4,
        "time": 10
    })
    assert response.status_code == 400
    assert response.json['error'] == "Missing field: type"


# Test: Invalid Data Types (Amount is not a float-compatible string)
def test_event_invalid_data_type(client):
    response = client.post('/event', json={
        "type": "deposit",
        "amount": "invalid",  # Invalid amount
        "user_id": 5,
        "time": 10
    })
    assert response.status_code == 400
    assert response.json['error'] == "Invalid amount. Must be a valid number."


# Test: Negative Amount (Should return 400 with an error message)
def test_event_negative_amount(client):
    response = client.post('/event', json={
        "type": "deposit",
        "amount": "-100.00",  # Negative amount
        "user_id": 6,
        "time": 10
    })
    assert response.status_code == 400
    assert response.json['error'] == "Amount cannot be negative."


# Test: Large Amount (No error, but still triggers an alert code for withdrawal over 100)
def test_event_large_amount(client):
    response = client.post('/event', json={
        "type": "withdraw",
        "amount": "9999999999.99",  # Large amount
        "user_id": 7,
        "time": 20  # Ensure the time is sequentially larger than previous events
    })

    # Log the response and status code for further debugging
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 200


# Test: Non-Sequential Time (Should return 400 with an error message)
def test_event_non_sequential_time(client):
    client.post('/event', json={"type": "deposit", "amount": "50.00", "user_id": 8, "time": 10})
    response = client.post('/event', json={"type": "deposit", "amount": "60.00", "user_id": 8, "time": 5})  # Time goes backward

    assert response.status_code == 400
    assert response.json['error'] == "Time must be sequential and increasing."


# Test: Empty Payload (Should return 400 for missing data)
def test_event_empty_payload(client):
    response = client.post('/event', json={})
    assert response.status_code == 400
    assert response.json['error'] == "Missing field: type"


# Test: 3 Consecutive Increasing Deposits (Should trigger alert code 300)
def test_event_three_consecutive_increasing_deposits(client):
    client.post('/event', json={"type": "deposit", "amount": "50.00", "user_id": 9, "time": 10})
    client.post('/event', json={"type": "deposit", "amount": "60.00", "user_id": 9, "time": 20})
    response = client.post('/event', json={"type": "deposit", "amount": "70.00", "user_id": 9, "time": 30})

    assert response.status_code == 200
    assert response.json['alert'] == True
    assert 300 in response.json['alert_codes']
    assert response.json['user_id'] == 9


# Test: Total Deposits Over 200 in 30 Seconds (Should trigger alert code 123)
def test_event_deposits_exceeding_200_in_30_seconds(client):
    client.post('/event', json={"type": "deposit", "amount": "100.00", "user_id": 10, "time": 10})
    client.post('/event', json={"type": "deposit", "amount": "120.00", "user_id": 10, "time": 25})
    response = client.post('/event', json={"type": "deposit", "amount": "100.00", "user_id": 10, "time": 30})

    assert response.status_code == 200
    assert response.json['alert'] == True
    assert 123 in response.json['alert_codes']
    assert response.json['user_id'] == 10


# Test: Deposits spread out over time should not trigger any alert
def test_event_deposits_spread_out_no_alert(client):
    client.post('/event', json={"type": "deposit", "amount": "100.00", "user_id": 11, "time": 10})
    response = client.post('/event', json={"type": "deposit", "amount": "120.00", "user_id": 11, "time": 45})

    assert response.status_code == 200
    assert response.json['alert'] == False
    assert response.json['alert_codes'] == []
    assert response.json['user_id'] == 11