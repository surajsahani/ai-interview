from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from loguru import logger

from api.conf.config import settings
from api.middleware.logging import LoggingMiddleware
from api.middleware.error_handler import http_exception_handler, validation_exception_handler
from api.router import health, test

# 配置日志
logger.add(
    settings.LOG_FILE,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    rotation="500 MB"
)

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)

# 添加中间件
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 注册路由
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(test.router, prefix=settings.API_V1_STR) 