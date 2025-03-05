from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Interview Test API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_FILE: str = "api/logs/api.log"

settings = Settings() 