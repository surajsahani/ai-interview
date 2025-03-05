from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from api.model.api.base import Response, ResponseCode

async def http_exception_handler(request: Request, exc):
    """Handle HTTP exceptions and log the error"""
    error_msg = f"HTTP error occurred: {exc.status_code} - {exc.detail}"
    logger.error(f"{error_msg}\nPath: {request.url.path}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(
            code=ResponseCode.FAILED,
            message=str(exc.detail),
            data=None
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc):
    """Handle validation errors and log the details"""
    error_details = exc.errors()
    error_msg = "Validation error occurred:"
    for error in error_details:
        logger.error(f"{error_msg}\n"
                    f"Location: {' -> '.join(error['loc'])}\n"
                    f"Type: {error['type']}\n"
                    f"Message: {error['msg']}\n"
                    f"Path: {request.url.path}")
    
    return JSONResponse(
        status_code=400,
        content=Response(
            code=ResponseCode.INVALID_PARAMS,
            message=str(error_details),
            data=None
        ).model_dump()
    ) 