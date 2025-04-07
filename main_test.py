import pytest
from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app from your main application file.

client = TestClient(app)

# Test case for the root endpoint
def test_read_root(): #get req to root To make sure your API is live and root endpoint returns the correct message.
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Library Management System API is running !"}

# Test case for the /users route
def test_users_route():
    response = client.get("/users")
    # Here we are assuming the /users route exists but does not yet have functionality
    assert response.status_code == 401  # Adjust the status code based on actual route implementation #To check if unauthenticated users are blocked from accessing sensitive user data.

# Test case for the /books route
def test_books_route():
    response = client.get("/books")
    assert response.status_code == 200 #Expects a 200 OK, meaning the route is publicly accessible (or your API allows it without login).

# Test case for the /transactions route
def test_transactions_route():
    response = client.get("/transactions")
    # Assuming no resources available in /transactions yet
    assert response.status_code == 401
