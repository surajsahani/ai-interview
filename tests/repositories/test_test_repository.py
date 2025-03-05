import pytest
from datetime import datetime, UTC
from api.model.db.test import Test
from api.repositories.test_repository import TestRepository

@pytest.fixture(autouse=True)
async def cleanup():
    """Clean up test data after each test"""
    yield
    Test.objects.delete()

@pytest.mark.asyncio
async def test_create_test():
    """Test creating a new test"""
    repo = TestRepository()
    test = Test(
        test_id="test001",
        type="coding",
        language="python",
        difficulty="medium",
        create_date=datetime.now(UTC)
    )
    
    result = await repo.create_test(test)
    assert result.test_id == "test001"
    assert result.type == "coding"

@pytest.mark.asyncio
async def test_get_test():
    """Test getting a test by ID"""
    # First create a test
    repo = TestRepository()
    test = Test(
        test_id="test001",
        type="coding",
        language="python",
        difficulty="medium",
        create_date=datetime.now(UTC)
    ).save()
    
    # Then try to get it
    result = await repo.get_test_by_id("test001")
    assert result is not None
    assert result.test_id == "test001" 