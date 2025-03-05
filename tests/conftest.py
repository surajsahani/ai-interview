import pytest
import warnings
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from api.main import app
from api.conf.config import Config

# Filter out warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="Call to deprecated create function FileDescriptor()"
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database connection"""
    config = Config.load_config()
    
    # Use a test database
    test_db = f"{config.mongodb.database}_test"
    
    # Connect to test database
    connect(
        db=test_db,
        host=config.mongodb.host,
        port=config.mongodb.port,
        username=config.mongodb.username,
        password=config.mongodb.password,
        authentication_source=config.mongodb.authentication_source
    )
    
    yield
    
    # Cleanup after tests
    disconnect()

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app) 