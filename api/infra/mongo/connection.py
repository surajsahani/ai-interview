from mongoengine import connect, disconnect
from loguru import logger
from api.conf.config import Config

def init_mongodb():
    """Initialize MongoDB connection"""
    config = Config.load_config()
    
    try:
        # Disconnect if already connected
        disconnect()
        
        # Connect to MongoDB
        connect(
            alias="default",
            db=config.mongodb.database,
            host=config.mongodb.host,
            port=config.mongodb.port,
            username=config.mongodb.username,
            password=config.mongodb.password,
            authentication_source=config.mongodb.authentication_source
        )
        logger.info(f"Connected to MongoDB: {config.mongodb.host}:{config.mongodb.port}/{config.mongodb.database}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise 