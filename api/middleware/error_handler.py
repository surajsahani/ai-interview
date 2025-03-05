from fastapi import Request
from fastapi.responses import JSONResponse
from api.model.base import Response, ResponseCode

async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=Response(
            code=ResponseCode.FAILED,
            message=str(exc.detail),
            data=None
        ).model_dump()
    )

async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content=Response(
            code=ResponseCode.INVALID_PARAMS,
            message=str(exc.errors()),
            data=None
        ).model_dump()
    ) 