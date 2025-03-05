from typing import Optional, List
from loguru import logger
from api.model.db.test import Test
from api.utils.log_decorator import log

class TestRepository:
    @log
    async def create_test(self, test: Test) -> Test:
        """Create a new test"""
        return test.save()
    
    @log
    async def get_test_by_id(self, test_id: str) -> Optional[Test]:
        """Get test by ID"""
        return Test.objects(test_id=test_id).first()
    
    @log
    async def get_tests_by_type(self, type: str) -> List[Test]:
        """Get tests by type"""
        return Test.objects(type=type).all()
    
    @log
    async def update_test(self, test: Test) -> Test:
        """Update test"""
        return test.save()
    
    @log
    async def delete_test(self, test_id: str) -> bool:
        """Delete test by ID"""
        result = Test.objects(test_id=test_id).delete()
        return result > 0 