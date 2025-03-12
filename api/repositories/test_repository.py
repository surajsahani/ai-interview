from typing import Optional, List
from loguru import logger
from api.model.db.test import Test, TestStatus
from api.utils.log_decorator import log
from datetime import datetime, UTC  
from mongoengine import Document, StringField, DateTimeField

class TestRepository:
    def __init__(self):
        # 假设你使用的是 MongoEngine
        self.collection = Test._get_collection()  # 获取底层的 MongoDB 集合

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
    
    @log
    async def update_test_status(self, test_id: str, status: TestStatus) -> Optional[Test]:
        """
        更新测试状态
        
        Args:
            test_id: 测试ID
            status: 新状态
            
        Returns:
            Optional[Test]: 更新后的测试文档，如果不存在则返回 None
        """
        try:
            test = Test.objects(test_id=test_id).first()
            if test:
                test.status = status.value
                test.update_date = datetime.now(UTC)
                if status == TestStatus.COMPLETED:
                    test.close_date = datetime.now(UTC)
                test.save()
                return test
            return None
        except Exception as e:
            logger.error(f"更新测试状态失败: {e}")
            raise 