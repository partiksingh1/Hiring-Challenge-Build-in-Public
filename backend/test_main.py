import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main2 import app

client = TestClient(app)

# Mock Firebase Authentication
@pytest.fixture
def mock_firebase_auth():
    with patch("firebase_admin.auth.create_user") as mock_create_user, \
         patch("firebase_admin.auth.get_user_by_email") as mock_get_user:
        
        # Mock the user creation and login
        mock_create_user.return_value = MagicMock(uid="test-user-123")
        mock_get_user.return_value = MagicMock(uid="test-user-123", email="test@example.com")
        
        yield mock_create_user, mock_get_user

# Tests for the Signup and Login Endpoints
def test_signup(mock_firebase_auth):
    """Test signup endpoint"""
    response = client.post("/signup", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "uid": "test-user-123"}

def test_login(mock_firebase_auth):
    """Test login endpoint"""
    response = client.post("/login", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "idToken" in response.json()
