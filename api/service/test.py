from api.model.api.test import CreateTestRequest, TestResponse
from api.model.db.test import Test
from api.repositories.test_repository import TestRepository
from api.utils.log_decorator import log

class TestService:
    def __init__(self):
        self.repository = TestRepository()
    
    @log
    async def create_test(self, request: CreateTestRequest) -> TestResponse:
        """
        Create a new test with the given parameters
        
        Args:
            request: The test creation request containing test details
            
        Returns:
            TestResponse: The created test response
        """
        # Create test document
        test = Test(
            test_id=request.test_id,
            type=request.type,
            language=request.language,
            difficulty=request.difficulty,
            create_date=request.create_date
        )
        
        # Save to database
        await self.repository.create_test(test)
        
        return TestResponse(
            test_id=test.test_id,
            status="created"
        ) 