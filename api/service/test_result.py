import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, UTC
from api.model.db.test_result import TestResult
from api.model.api.test_result import TestResultResponse, CreateTestResultRequest
from api.repositories.test_result_repository import TestResultRepository
from api.repositories.test_repository import TestRepository
from api.repositories.user_repository import UserRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, ValidationError
from loguru import logger

class TestResultService:
    """测试结果服务类"""
    
    def __init__(self):
        """初始化测试结果服务"""
        self.repository = TestResultRepository()
        self.test_repository = TestRepository()
        self.user_repository = UserRepository()
    
    @log
    async def create_test_result(self, request: CreateTestResultRequest) -> TestResultResponse:
        """
        创建或更新测试结果
        
        Args:
            request: 创建测试结果请求
            
        Returns:
            TestResultResponse: 测试结果响应
            
        Raises:
            NotFoundError: 如果测试或用户不存在
        """
        # 检查测试是否存在
        test = await self.test_repository.get_test_by_id(request.test_id)
        if not test:
            raise NotFoundError(f"测试不存在: {request.test_id}")
        
        # 检查用户是否存在
        user = await self.user_repository.get_user_by_id(request.user_id)
        if not user:
            raise NotFoundError(f"用户不存在: {request.user_id}")
        
        # 检查是否已存在该测试的结果
        existing_result = await self.repository.get_result_by_test_id(request.test_id)
        
        # 验证数据
        if request.score < 0 or request.score > 100:
            raise ValidationError("分数必须在0-100之间")
        
        if request.question_number < 0:
            raise ValidationError("问题数不能为负")
            
        if request.correct_number < 0:
            raise ValidationError("正确答案数不能为负")
            
        if request.correct_number > request.question_number:
            raise ValidationError("正确答案数不能大于问题总数")
            
        if request.elapse_time < 0:
            raise ValidationError("耗时不能为负")
        
        if existing_result:
            # 如果已存在结果，则更新它
            logger.info(f"已存在测试结果，进行更新: {existing_result.test_id}")
            
            # 更新字段
            existing_result.summary = request.summary
            existing_result.score = request.score
            existing_result.question_number = request.question_number
            existing_result.correct_number = request.correct_number
            existing_result.elapse_time = request.elapse_time
            existing_result.qa_history = request.qa_history
            
            # 保存更新
            updated_result = await self.repository.create_result(existing_result)
            logger.info(f"更新测试结果完成: {existing_result.test_id}")
            
            return self._to_response(updated_result)
        else:
            # 如果不存在结果，则创建新的
            test_result = TestResult(
                test_id=request.test_id,
                user_id=request.user_id,
                summary=request.summary,
                score=request.score,
                question_number=request.question_number,
                correct_number=request.correct_number,
                elapse_time=request.elapse_time,
                qa_history=request.qa_history
            )
            
            # 保存到数据库
            created_result = await self.repository.create_result(test_result)
            logger.info(f"创建新的测试结果: {request.test_id}")
            
            return self._to_response(created_result)
    
    @log
    async def get_test_result_by_test_id(self, test_id: str) -> TestResultResponse:
        """
        根据测试ID获取测试结果
        
        Args:
            test_id: 测试ID
            
        Returns:
            TestResultResponse: 测试结果响应
            
        Raises:
            NotFoundError: 如果测试结果不存在
        """
        test_result = await self.repository.get_result_by_test_id(test_id)
        if not test_result:
            raise NotFoundError(f"该测试没有相关结果: {test_id}")
        
        return self._to_response(test_result)
    
    @log
    async def get_test_results_by_user_id(self, user_id: str) -> List[TestResultResponse]:
        """
        根据用户ID获取测试结果列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[TestResultResponse]: 测试结果响应列表
        """
        test_results = await self.repository.get_results_by_user_id(user_id)
        return [self._to_response(result) for result in test_results]
    
    def _to_response(self, test_result: TestResult) -> TestResultResponse:
        """
        将TestResult文档转换为TestResultResponse
        
        Args:
            test_result: 测试结果文档
            
        Returns:
            TestResultResponse: 测试结果响应
        """
        return TestResultResponse(
            test_id=test_result.test_id,
            user_id=test_result.user_id,
            summary=test_result.summary,
            score=test_result.score,
            question_number=test_result.question_number,
            correct_number=test_result.correct_number,
            elapse_time=test_result.elapse_time,
            qa_history=test_result.qa_history
        )

