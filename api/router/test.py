from fastapi import APIRouter, HTTPException
from api.model.test import CreateTestRequest, TestResponse
from api.model.base import Response
from api.service.test import TestService

router = APIRouter()
test_service = TestService()

@router.post("/test", response_model=Response[TestResponse])
async def create_test(request: CreateTestRequest):
    """
    Create a new test with specified parameters
    """
    try:
        result = await test_service.create_test(request)
        return Response[TestResponse](data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 