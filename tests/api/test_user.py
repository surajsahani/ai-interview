import pytest
from datetime import datetime, UTC
from httpx import AsyncClient
from api.model.db.user import User
from api.main import app

@pytest.fixture(autouse=True)
async def cleanup():
    """Clean up test data after each test"""
    yield
    User.objects.delete()

@pytest.fixture
def user_data():
    """Test user data"""
    return {
        "user_name": "test_user",
        "password": "test_password",
        "email": "test@example.com",
        "staff_id": "STAFF001",
        "role": 1
    }

@pytest.fixture
async def test_user(user_data):
    """Create a test user"""
    user = User(
        user_id="test001",
        user_name=user_data["user_name"],
        password="hashed_password",
        email=user_data["email"],
        staff_id=user_data["staff_id"],
        role=user_data["role"],
        status=0,
        create_date=datetime.now(UTC)
    ).save()
    return user

async def test_create_user(user_data):
    """Test user creation"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/user", json=user_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["user_name"] == user_data["user_name"]
        assert data["email"] == user_data["email"]
        assert data["staff_id"] == user_data["staff_id"]
        assert data["role"] == user_data["role"]
        assert data["status"] == 0  # default active status

async def test_create_user_duplicate_email(user_data, test_user):
    """Test user creation with duplicate email"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/user", json=user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["message"]

async def test_get_user(test_user):
    """Test getting a user by ID"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/v1/user/{test_user.user_id}")
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["user_id"] == test_user.user_id
        assert data["user_name"] == test_user.user_name
        assert data["email"] == test_user.email

async def test_get_user_not_found():
    """Test getting a non-existent user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/user/nonexistent")
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]

async def test_get_users(test_user):
    """Test getting users with pagination"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/user?skip=0&limit=10")
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["user_id"] == test_user.user_id

async def test_update_user(test_user):
    """Test updating a user"""
    update_data = {
        "user_name": "updated_name",
        "email": "updated@example.com",
        "status": 1
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            f"/api/v1/user/{test_user.user_id}",
            json=update_data
        )
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["user_name"] == update_data["user_name"]
        assert data["email"] == update_data["email"]
        assert data["status"] == update_data["status"]

async def test_update_user_not_found():
    """Test updating a non-existent user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "/api/v1/user/nonexistent",
            json={"user_name": "new_name"}
        )
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]

async def test_delete_user(test_user):
    """Test deleting a user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/api/v1/user/{test_user.user_id}")
        assert response.status_code == 200
        assert response.json()["data"]["deleted"] is True
        
        # Verify user is deleted
        response = await ac.get(f"/api/v1/user/{test_user.user_id}")
        assert response.status_code == 404

async def test_delete_user_not_found():
    """Test deleting a non-existent user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/api/v1/user/nonexistent")
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]

async def test_create_user_invalid_data():
    """Test user creation with invalid data"""
    invalid_data = {
        "user_name": "test_user",
        "password": "test_password",
        "email": "invalid_email",  # Invalid email format
        "role": 3  # Invalid role value
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/user", json=invalid_data)
        assert response.status_code == 422  # Validation error 