from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.test import CreateTestRequest, UpdateTestRequest, TestResponse
from api.service.test import TestService
from api.constants.common import TestType
# from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError, ValidationError
from loguru import logger

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[TestResponse])
async def create_test(request: CreateTestRequest):
    """
    创建新测试
    
    - **test_id**: 测试ID
    - **type**: 测试类型
    - **language**: 语言
    - **difficulty**: 难度
    - **job_id**: 关联的职位ID（可选）
    - **user_id**: 关联的用户ID（可选）
    - **question_ids**: 测试包含的问题ID列表（可选）
    """
    service = TestService()
    test = await service.create_test(request)
    return Response[TestResponse](data=test)

@router.get("/{test_id}", response_model=Response[TestResponse])
async def get_test(test_id: str):
    """
    根据ID获取测试
    
    - **test_id**: 测试ID
    """
    service = TestService()
    test = await service.get_test(test_id)
    return Response[TestResponse](data=test)

@router.get("", response_model=Response[List[TestResponse]])
async def get_tests(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    获取测试列表（分页）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = TestService()
    tests = await service.get_tests(skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.put("/{test_id}", response_model=Response[TestResponse])
async def update_test(test_id: str, request: UpdateTestRequest):
    """
    更新测试
    
    - **test_id**: 测试ID
    - **type**: 测试类型（可选）
    - **language**: 语言（可选）
    - **difficulty**: 难度（可选）
    - **status**: 测试状态（可选）
    - **job_id**: 关联的职位ID（可选）
    - **user_id**: 关联的用户ID（可选）
    - **question_ids**: 测试包含的问题ID列表（可选）
    """
    service = TestService()
    test = await service.update_test(test_id, request)
    return Response[TestResponse](data=test)

@router.delete("/{test_id}", response_model=Response[dict])
async def delete_test(test_id: str):
    """
    删除测试
    
    - **test_id**: 测试ID
    """
    service = TestService()
    deleted = await service.delete_test(test_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/user/{user_id}", response_model=Response[List[TestResponse]])
async def get_tests_by_user_id(
    user_id: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据用户ID获取测试
    
    - **user_id**: 用户ID
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = TestService()
    tests = await service.get_tests_by_user_id(user_id, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/job/{job_id}", response_model=Response[List[TestResponse]])
async def get_tests_by_job_id(
    job_id: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据职位ID获取测试
    
    - **job_id**: 职位ID
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = TestService()
    tests = await service.get_tests_by_job_id(job_id, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/status/{status}", response_model=Response[List[TestResponse]])
async def get_tests_by_status(
    status: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据状态获取测试
    
    - **status**: 测试状态
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = TestService()
    tests = await service.get_tests_by_status(status, skip, limit)
    return Response[List[TestResponse]](data=tests)

@router.get("/type/{type}", response_model=Response[List[TestResponse]])
async def get_tests_by_type(
    type: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据类型获取测试
    
    - **type**: 测试类型，可选值: interview, coding, behavior
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    if type not in TestType.choices():
        raise HTTPException(status_code=400, detail=f"无效的测试类型: {type}")
    
    service = TestService()
    tests = await service.get_tests_by_type(type, skip, limit)
    return Response[List[TestResponse]](data=tests) 

@router.get("/activate_code/{code}", response_model=Response[TestResponse])
async def get_test_by_activate_code(code: str):
    """
    根据激活码获取测试
    
    - **code**: 测试激活码
    
    只返回状态不是已完成的测试
    """
    try:
        service = TestService()
        test = await service.get_test_by_activate_code(code)
        return Response[TestResponse](
            code="0",
            message="success",
            data=test
        )
    except NotFoundError as e:
        logger.warning(f"NotFoundError 获取测试失败: {str(e)}, 激活码: {code}")
        return Response[TestResponse](
            code="404",
            message=str(e),
            data=None
        )
    except Exception as e:
        logger.error(f"Exception 获取测试失败: {e}, 激活码: {code}")
        raise HTTPException(status_code=500, detail=str(e))