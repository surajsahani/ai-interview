import pytest
import uuid
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC

from api.model.db.test_result import TestResult
from api.model.api.test_result import CreateTestResultRequest
from api.service.test_result import TestResultService
from api.exceptions.api_error import NotFoundError, ValidationError

@pytest.mark.asyncio
async def test_create_test_result_new():
    """测试创建新的测试结果"""
    # 创建请求数据
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    request = CreateTestResultRequest(
        test_id=test_id,
        user_id=user_id,
        summary="测试总结",
        score=85.5,
        question_number=10,
        correct_number=8,
        elapse_time=30,
        qa_history=[
            {"question": "什么是Python?", "answer": "Python是一种高级编程语言"},
            {"question": "什么是FastAPI?", "answer": "FastAPI是一个现代化的Python Web框架"}
        ]
    )
    
    # Mock测试和用户存在性检查
    with patch('api.repositories.test_repository.TestRepository.get_test_by_id') as mock_get_test, \
         patch('api.repositories.user_repository.UserRepository.get_user_by_id') as mock_get_user, \
         patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get_result, \
         patch('api.repositories.test_result_repository.TestResultRepository.create_result') as mock_create:
        
        # 设置Mock返回值
        mock_get_test.return_value = MagicMock(test_id=test_id)
        mock_get_user.return_value = MagicMock(user_id=user_id)
        mock_get_result.return_value = None  # 不存在现有结果
        
        # 设置创建结果的返回值
        created_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="测试总结",
            score=85.5,
            question_number=10,
            correct_number=8,
            elapse_time=30,
            qa_history=[
                {"question": "什么是Python?", "answer": "Python是一种高级编程语言"},
                {"question": "什么是FastAPI?", "answer": "FastAPI是一个现代化的Python Web框架"}
            ]
        )
        mock_create.return_value = created_result
        
        # 调用服务方法
        service = TestResultService()
        result = await service.create_test_result(request)
        
        # 验证结果
        assert result.test_id == test_id
        assert result.user_id == user_id
        assert result.summary == "测试总结"
        assert result.score == 85.5
        assert result.question_number == 10
        assert result.correct_number == 8
        assert result.elapse_time == 30
        assert len(result.qa_history) == 2
        
        # 验证方法调用
        mock_get_test.assert_called_once_with(test_id)
        mock_get_user.assert_called_once_with(user_id)
        mock_get_result.assert_called_once_with(test_id)
        mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_create_test_result_update_existing():
    """测试更新已存在的测试结果"""
    # 创建请求数据
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    request = CreateTestResultRequest(
        test_id=test_id,
        user_id=user_id,
        summary="更新后的总结",
        score=90.0,
        question_number=10,
        correct_number=9,
        elapse_time=25,
        qa_history=[
            {"question": "问题1", "answer": "回答1"},
            {"question": "问题2", "answer": "回答2"}
        ]
    )
    
    # Mock测试和用户存在性检查
    with patch('api.repositories.test_repository.TestRepository.get_test_by_id') as mock_get_test, \
         patch('api.repositories.user_repository.UserRepository.get_user_by_id') as mock_get_user, \
         patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get_result, \
         patch('api.repositories.test_result_repository.TestResultRepository.create_result') as mock_update:
        
        # 设置Mock返回值
        mock_get_test.return_value = MagicMock(test_id=test_id)
        mock_get_user.return_value = MagicMock(user_id=user_id)
        
        # 设置已存在的结果
        existing_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="原有总结",
            score=85.0,
            question_number=10,
            correct_number=7,
            elapse_time=30,
            qa_history=[{"question": "旧问题", "answer": "旧回答"}]
        )
        mock_get_result.return_value = existing_result
        
        # 设置更新结果的返回值
        updated_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="更新后的总结",
            score=90.0,
            question_number=10,
            correct_number=9,
            elapse_time=25,
            qa_history=[
                {"question": "问题1", "answer": "回答1"},
                {"question": "问题2", "answer": "回答2"}
            ]
        )
        mock_update.return_value = updated_result
        
        # 调用服务方法
        service = TestResultService()
        result = await service.create_test_result(request)
        
        # 验证结果
        assert result.test_id == test_id
        assert result.summary == "更新后的总结"
        assert result.score == 90.0
        assert result.question_number == 10
        assert result.correct_number == 9
        assert result.elapse_time == 25
        assert len(result.qa_history) == 2
        
        # 验证方法调用
        mock_get_result.assert_called_once_with(test_id)
        mock_update.assert_called_once()



@pytest.mark.asyncio
async def test_get_test_result_by_test_id():
    """测试根据测试ID获取测试结果"""
    test_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    # Mock仓库方法
    with patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get:
        # 设置Mock返回值
        test_result = TestResult(
            test_id=test_id,
            user_id=user_id,
            summary="测试总结",
            score=85.5,
            question_number=10,
            correct_number=8,
            elapse_time=30,
            qa_history=[{"question": "问题", "answer": "回答"}]
        )
        mock_get.return_value = test_result
        
        # 调用服务方法
        service = TestResultService()
        result = await service.get_test_result_by_test_id(test_id)
        
        # 验证结果
        assert result.test_id == test_id
        assert result.user_id == user_id
        assert result.summary == "测试总结"
        assert result.score == 85.5
        assert result.question_number == 10
        assert result.correct_number == 8
        assert result.elapse_time == 30
        
        # 验证方法调用
        mock_get.assert_called_once_with(test_id)

@pytest.mark.asyncio
async def test_get_test_result_by_test_id_not_found():
    """测试获取不存在的测试结果"""
    test_id = str(uuid.uuid4())
    
    # Mock仓库方法
    with patch('api.repositories.test_result_repository.TestResultRepository.get_result_by_test_id') as mock_get:
        # 设置Mock返回值
        mock_get.return_value = None
        
        # 调用服务方法并验证异常
        service = TestResultService()
        with pytest.raises(NotFoundError) as excinfo:
            await service.get_test_result_by_test_id(test_id)
        
        # 验证异常消息
        assert "该测试没有相关结果" in str(excinfo.value)
        
        # 验证方法调用
        mock_get.assert_called_once_with(test_id)

@pytest.mark.asyncio
async def test_get_test_results_by_user_id():
    """测试根据用户ID获取测试结果列表"""
    user_id = str(uuid.uuid4())
    
    # Mock仓库方法
    with patch('api.repositories.test_result_repository.TestResultRepository.get_results_by_user_id') as mock_get:
        # 设置Mock返回值
        test_results = [
            TestResult(
                test_id=str(uuid.uuid4()),
                user_id=user_id,
                summary="测试总结1",
                score=85.5,
                question_number=10,
                correct_number=8,
                elapse_time=30,
                qa_history=[]
            ),
            TestResult(
                test_id=str(uuid.uuid4()),
                user_id=user_id,
                summary="测试总结2",
                score=90.0,
                question_number=10,
                correct_number=9,
                elapse_time=25,
                qa_history=[]
            )
        ]
        mock_get.return_value = test_results
        
        # 调用服务方法
        service = TestResultService()
        results = await service.get_test_results_by_user_id(user_id)
        
        # 验证结果
        assert len(results) == 2
        assert all(r.user_id == user_id for r in results)
        assert results[0].summary == "测试总结1"
        assert results[1].summary == "测试总结2"
        
        # 验证方法调用
        mock_get.assert_called_once_with(user_id)