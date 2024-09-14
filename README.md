# Midnite Junior Backend Engineer Technical Task

## Project Overview

This project is a backend service with a single `/event` API endpoint that accepts user actions such as deposits and withdrawals. Based on these actions, the API raises alerts according to specific rules, as outlined in the task description.

---

## Features Implemented
- **/event** API endpoint that accepts POST requests with a payload containing user actions.
- **Alert conditions**:
  - **Code 1100**: Triggered when a withdrawal amount exceeds 100.
  - **Code 30**: Triggered after 3 consecutive withdrawals.
  - **Code 300**: Triggered after 3 consecutive deposits where each is larger than the previous one.
  - **Code 123**: Triggered when the total deposit amount exceeds 200 within 30 seconds.
  
---

## Requirements

To run the project, you need:
- Python 3.9+ installed.
- Flask for the web framework.
- Pytest for testing.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd midnite_take_home 
   ```

2. **Create a Virtual Environment (Optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
   ```
3. **Install Dependencies: Install all the required dependencies via `pip`:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Flask Application: Start the Flask server on your local machine:**
   ```bash
   python app.py
   ```
   The server will be running on http://127.0.0.1:5000.

---
## Usage
You can test the API using `curl` commands or any API testing tool such as Postman.

### Example Requests:
- Deposit Request (No Alert Expected):
    ```bash
    curl -X POST http://127.0.0.1:5000/event -H "Content-Type: application/json" -d '{"type": "deposit", "amount": "50.00", "user_id": 1, "time": 10}'
    ```
- Withdrawal Request (Triggers Alert Code 1100):
    ```bash 
    curl -X POST http://127.0.0.1:5000/event -H "Content-Type: application/json" -d '{"type": "withdraw", "amount": "150.00", "user_id": 1, "time": 20}'
    ```
- Deposit Exceeding 200 within 30 seconds (Triggers Alert Code 123):
    ```bash 
    curl -X POST http://127.0.0.1:5000/event -H "Content-Type: application/json" -d '{"type": "deposit", "amount": "100.00", "user_id": 1, "time": 10}'
    curl -X POST http://127.0.0.1:5000/event -H "Content-Type: application/json" -d '{"type": "deposit", "amount": "120.00", "user_id": 1, "time": 20}'
    ```
---
## Running Tests
Unit tests are written using pytest. To run the tests:
1. Ensure you are in the project root directory.
2. Run the following command:
    ```bash 
    pytest
    ```
This will run all test cases in the `tests/` folder. The tests cover various alert conditions, including:
- Deposit and withdrawal scenarios.
- Handling consecutive actions.
- Edge cases like negative amounts, large values, etc.

---
### File Structure 
```
.
├── app/
│   ├── __init__.py        # Initializes the Flask app
│   └── routes.py          # Contains the /event API logic
├── tests/
│   └── test_event.py      # Unit tests for the API
├── .gitignore             # Files and directories to be ignored by Git
├── app.py                 # Main file to run the Flask app
├── LICENSE                # MIT License details here
├── README.md              # This file
└── requirements.txt       # Project dependencies
```
---
## Challenges Faced

### 1. Handling Invalid or Missing Data
One of the main challenges was ensuring that the API handled cases where the payload had missing or invalid fields. Initially, the API would return a `500 Internal Server Error` due to uncaught `KeyError` exceptions when trying to access fields like `type` or `amount` when they were not present in the request payload. 

**Solution**: We added validation to check for required fields before processing the request, ensuring that the API returns proper error responses (such as `400 Bad Request`) for missing or invalid data.

### 2. Testing with Pytest
Some of the test cases initially failed, especially when testing edge cases like missing fields, invalid data types, negative amounts, and large values. These issues were primarily due to the API not handling exceptions properly, which resulted in `500 Internal Server Errors` instead of expected `400 Bad Request` responses.

**Solution**: We adjusted the API to handle exceptions more gracefully and ensure that invalid inputs were caught early in the request processing pipeline, allowing the tests to pass successfully.

### 3. Understanding How to Use Curl
Initially, there was confusion about how to use `curl` for testing the API endpoints. The Flask server needed to be running in the background while `curl` commands were executed from another terminal, which was unclear at first.

**Solution**: After troubleshooting, we confirmed that the Flask app needed to be running in one terminal, and the `curl` commands should be executed in a separate terminal window. Once this was understood, testing with `curl` worked as expected.

### 4. Implementing Consecutive Event Logic
Another challenge was correctly implementing the logic for tracking consecutive deposits and withdrawals. For example, detecting when three consecutive withdrawals occur or when three consecutive deposits increase in amount was tricky because the system had to track the history of user actions.

**Solution**: We used an in-memory dictionary to store user actions, ensuring that consecutive actions could be tracked efficiently without a database. This approach worked for the scope of this project, but for a larger-scale system, a persistent storage solution like a database or a caching system like Redis would be more appropriate.

### 5. Edge Case Handling
We encountered edge cases, such as handling negative amounts, non-sequential timestamps, and large values, which initially caused the system to behave unexpectedly or fail. For instance, negative withdrawal amounts or very large deposit amounts weren't handled properly, causing exceptions.

**Solution**: Input validation was added to ensure that such edge cases were properly handled, and tests were written to verify that the system responded correctly to these scenarios.



---
## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
## Author 
Bilal Fawaz 