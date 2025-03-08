from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger
import uvicorn

from api.conf.config import Config
from api.infra.mongo.connection import init_mongodb
from api.middleware.logging import LoggingMiddleware
from api.middleware.error_handler import (
    api_error_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from api.router import health, test, user, job
from api.exceptions.api_error import APIError

# Load configuration
config = Config.load_config()

# Initialize MongoDB
init_mongodb()

# Configure logging
logger.add(
    config.logging.file,
    level=config.logging.level,
    format=config.logging.format,
    rotation=config.logging.rotation
)

app = FastAPI(
    title=config.app.name,
    openapi_url=f"{config.app.api_v1_str}/openapi.yaml",
    docs_url=f"{config.app.api_v1_str}/doc",
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_credentials=config.cors.allow_credentials,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
)

# Register exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Register routers
app.include_router(health.router, prefix=config.app.api_v1_str)
app.include_router(test.router, prefix=config.app.api_v1_str)
app.include_router(user.router, prefix=config.app.api_v1_str)
app.include_router(job.router, prefix=config.app.api_v1_str)

# Run the API server
# uvicorn api.main:app --reload
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload
    ) 