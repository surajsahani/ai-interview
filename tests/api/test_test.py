import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from api.main import app

client = TestClient(app)

def test_create_test(client):
    """Test successful test creation"""
    test_data = {
        "test_id": "test001",
        "type": "coding",
        "language": "python",
        "difficulty": "medium",
        "create_date": datetime.now().isoformat()
    }
    
    response = client.post("/api/v1/test", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["code"] == "0"
    assert data["data"]["test_id"] == "test001"
    assert data["data"]["status"] == "created"

def test_create_test_invalid_params(client):
    """Test validation error handling"""
    test_data = {
        "test_id": "test001",
        "type": "invalid_type",  # Invalid type
        "language": "python",
        "difficulty": "medium",
        "create_date": datetime.now().isoformat()
    }
    
    response = client.post("/api/v1/test", json=test_data)
    assert response.status_code == 400  # Changed from 422 to match error handler 