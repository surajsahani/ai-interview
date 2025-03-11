from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.test_result import CreateTestResultRequest, UpdateTestResultRequest, TestResultResponse
from api.service.test_result import TestResultService
from api.exceptions.api_error import NotFoundError, ValidationError
from loguru import logger

router = APIRouter(
    prefix="/test_result",
    tags=["test_result"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[TestResultResponse])
async def create_test_result(request: CreateTestResultRequest):
    """
    创建或更新测试结果
    
    - **test_id**: 测试ID
    - **user_id**: 用户ID
    - **summary**: 总结
    - **score**: 分数 (0-100)
    - **question_number**: 问题数量
    - **correct_number**: 正确答案数量
    - **elapse_time**: 耗时(分钟)
    - **qa_history**: 问答历史
    """
    try:
        service = TestResultService()
        result = await service.create_test_result(request)
        return Response[TestResultResponse](
            code="0",
            message="success",
            data=result
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError 创建测试结果失败: {str(e)}")
        return Response[TestResultResponse](
            code="404",
            message=str(e),
            data=None
        )
    except ValidationError as e:
        logger.warning(f"ValidationError 创建测试结果失败: {str(e)}")
        return Response[TestResultResponse](
            code="400",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception 创建测试结果失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test/{test_id}", response_model=Response[TestResultResponse])
async def get_test_result_by_test_id(test_id: str):
    """
    根据测试ID获取测试结果
    
    - **test_id**: 测试ID
    """
    try:
        service = TestResultService()
        result = await service.get_test_result_by_test_id(test_id)
        return Response[TestResultResponse](
            code="0",
            message="success",
            data=result
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError 获取测试结果失败: {str(e)}, 测试ID: {test_id}")
        return Response[TestResultResponse](
            code="404",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception 获取测试结果失败: {e}, 测试ID: {test_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=Response[List[TestResultResponse]])
async def get_test_results_by_user_id(user_id: str):
    """
    根据用户ID获取测试结果列表
    
    - **user_id**: 用户ID
    """
    try:
        service = TestResultService()
        results = await service.get_test_results_by_user_id(user_id)
        return Response[List[TestResultResponse]](
            code="0",
            message="success",
            data=results
        )
    except Exception as e:
        logger.error(f"Exception 获取用户测试结果失败: {e}, 用户ID: {user_id}")
        raise HTTPException(status_code=500, detail=str(e))