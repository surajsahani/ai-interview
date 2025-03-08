from typing import Optional, List
from loguru import logger
from api.model.db.test import Test
from api.utils.log_decorator import log

class TestRepository:
    @log
    async def create_test(self, test: Test) -> Test:
        """创建新测试"""
        return test.save()
    
    @log
    async def get_test_by_id(self, test_id: str) -> Optional[Test]:
        """根据ID获取测试"""
        return Test.objects(test_id=test_id).first()
    
    @log
    async def get_tests(self, skip: int = 0, limit: int = 100) -> List[Test]:
        """获取测试列表（分页）"""
        return Test.objects().skip(skip).limit(limit).all()
    
    @log
    async def update_test(self, test: Test) -> Test:
        """更新测试"""
        return test.save()
    
    @log
    async def delete_test(self, test_id: str) -> bool:
        """删除测试"""
        result = Test.objects(test_id=test_id).delete()
        return result > 0
    
    @log
    async def get_tests_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """根据用户ID获取测试"""
        return Test.objects(user_id=user_id).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_job_id(self, job_id: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """根据职位ID获取测试"""
        return Test.objects(job_id=job_id).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """根据状态获取测试"""
        return Test.objects(status=status).skip(skip).limit(limit).all()
    
    @log
    async def get_tests_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[Test]:
        """根据类型获取测试"""
        return Test.objects(type=type).skip(skip).limit(limit).all()
    
    @log
    async def get_test_by_activate_code(self, activate_code: str) -> Optional[Test]:
        """根据激活码获取测试"""
        return Test.objects(activate_code=activate_code).first() 