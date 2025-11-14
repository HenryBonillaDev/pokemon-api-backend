import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app

client = TestClient(app)

@patch('app.repositories.user_repository.user_repository.create_user')
@patch('app.repositories.user_repository.user_repository.get_user_by_username')
@patch('app.repositories.user_repository.user_repository.get_user_by_email')
def test_register_user(mock_get_email, mock_get_user, mock_create):
    mock_get_user.return_value = None
    mock_get_email.return_value = None
    
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.email = "test@example.com"
    mock_user.disabled = False
    
    mock_create.return_value = mock_user
    
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 201