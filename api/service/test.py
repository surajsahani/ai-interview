import uuid
import random
import string
from typing import List, Optional
from datetime import datetime, UTC, timedelta
from api.model.api.test import CreateTestRequest, UpdateTestRequest, TestResponse
from api.model.db.test import Test
from api.repositories.test_repository import TestRepository
from api.repositories.job_repository import JobRepository
from api.repositories.user_repository import UserRepository
from api.repositories.question_repository import QuestionRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError, ValidationError
from api.constants.common import TestStatus, TestType, Language, Difficulty

class TestService:
    def __init__(self):
        self.repository = TestRepository()
        self.job_repository = JobRepository()
        self.user_repository = UserRepository()
        self.question_repository = QuestionRepository()
    
    def _generate_activate_code(self, length=10) -> str:
        """生成指定长度的数字激活码"""
        return ''.join(random.choices(string.digits, k=length))
    
    async def _is_activate_code_unique(self, code: str) -> bool:
        """检查激活码是否唯一"""
        test = await self.repository.get_test_by_activate_code(code)
        return test is None
    
    async def _generate_unique_activate_code(self, length=10) -> str:
        """生成唯一的激活码"""
        max_attempts = 10  # 最大尝试次数
        for _ in range(max_attempts):
            code = self._generate_activate_code(length)
            if await self._is_activate_code_unique(code):
                return code
        
        # 如果多次尝试后仍未生成唯一激活码，则使用更长的激活码
        return await self._generate_unique_activate_code(length + 1)
    
    @log
    async def create_test(self, request: CreateTestRequest) -> TestResponse:
        """创建新测试"""
        # 验证测试类型
        if request.type not in TestType.choices():
            raise ValidationError(f"无效的测试类型: {request.type}")
        
        # 验证语言
        if request.language not in Language.choices():
            raise ValidationError(f"无效的语言: {request.language}")
        
        # 验证难度
        if request.difficulty not in Difficulty.choices():
            raise ValidationError(f"无效的难度: {request.difficulty}")
        
        # 生成唯一ID
        test_id = str(uuid.uuid4())
        
        # 生成唯一激活码
        activate_code = await self._generate_unique_activate_code()
        
        # 获取Job信息
        job_title = None
        if request.job_id:
            job = await self.job_repository.get_job_by_id(request.job_id)
            if job:
                job_title = job.job_title
        
        # 获取User信息
        user_name = None
        if request.user_id:
            user = await self.user_repository.get_user_by_id(request.user_id)
            if user:
                user_name = user.user_name
        
        # 自动生成问题列表
        question_ids = []
        if not request.question_ids:
            question_ids = await self._generate_questions(
                job_title, 
                request.language, 
                request.difficulty, 
                request.examination_points or []
            )
        else:
            question_ids = request.question_ids
        
        # 创建测试文档
        test = Test(
            test_id=test_id,
            activate_code=activate_code,
            type=request.type,
            language=request.language,
            difficulty=request.difficulty,
            status=TestStatus.OPEN,
            job_id=request.job_id,
            job_title=job_title,
            user_id=request.user_id,
            user_name=user_name,
            question_ids=question_ids,
            examination_points=request.examination_points or [],
            test_time=request.test_time or 60,  # 默认60分钟
            create_date=datetime.now(UTC),
            start_date=datetime.now(UTC),
            expire_date=datetime.now(UTC) + timedelta(days=7),  # 默认7天后过期
            update_date=None
        )
        
        # 保存到数据库
        test = await self.repository.create_test(test)
        
        return self._to_response(test)
    
    @log
    async def get_test(self, test_id: str) -> TestResponse:
        """根据ID获取测试"""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("测试不存在")
        
        return self._to_response(test)
    
    @log
    async def get_tests(self, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """获取测试列表（分页）"""
        tests = await self.repository.get_tests(skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def update_test(self, test_id: str, request: UpdateTestRequest) -> TestResponse:
        """更新测试"""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("测试不存在")
        
        # 更新提供的字段
        if request.type is not None:
            test.type = request.type
        if request.language is not None:
            test.language = request.language
        if request.difficulty is not None:
            test.difficulty = request.difficulty
        if request.status is not None:
            test.status = request.status
        if request.job_id is not None:
            test.job_id = request.job_id
        if request.user_id is not None:
            test.user_id = request.user_id
        if request.question_ids is not None:
            test.question_ids = request.question_ids
        if request.examination_points is not None:
            test.examination_points = request.examination_points
        if request.test_time is not None:
            test.test_time = request.test_time
        
        # 更新时间
        test.update_date = datetime.now(UTC)
        
        test = await self.repository.update_test(test)
        return self._to_response(test)
    
    @log
    async def delete_test(self, test_id: str) -> bool:
        """删除测试"""
        test = await self.repository.get_test_by_id(test_id)
        if not test:
            raise NotFoundError("测试不存在")
        
        return await self.repository.delete_test(test_id)
    
    @log
    async def get_tests_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """根据用户ID获取测试"""
        tests = await self.repository.get_tests_by_user_id(user_id, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_job_id(self, job_id: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """根据职位ID获取测试"""
        tests = await self.repository.get_tests_by_job_id(job_id, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """根据状态获取测试"""
        tests = await self.repository.get_tests_by_status(status, skip, limit)
        return [self._to_response(test) for test in tests]
    
    @log
    async def get_tests_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[TestResponse]:
        """根据类型获取测试"""
        tests = await self.repository.get_tests_by_type(type, skip, limit)
        return [self._to_response(test) for test in tests]
    
    def _to_response(self, test: Test) -> TestResponse:
        """将Test文档转换为TestResponse"""
        return TestResponse(
            test_id=test.test_id,
            activate_code=test.activate_code,
            type=test.type,
            language=test.language,
            difficulty=test.difficulty,
            status=test.status,
            job_id=test.job_id,
            job_title=test.job_title,
            user_id=test.user_id,
            user_name=test.user_name,
            question_ids=test.question_ids,
            examination_points=test.examination_points,
            test_time=test.test_time,
            create_date=test.create_date,
            start_date=test.start_date,
            expire_date=test.expire_date,
            update_date=test.update_date
        ) 