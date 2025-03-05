from api.model.api.test import CreateTestRequest, TestResponse
from api.utils.log_decorator import log

class TestService:
    @log
    async def create_test(self, request: CreateTestRequest) -> TestResponse:
        """
        Create a new test with the given parameters
        
        Args:
            request: The test creation request containing test details
            
        Returns:
            TestResponse: The created test response
        """
        # 这里实现具体的业务逻辑
        return TestResponse(
            test_id=request.test_id,
            status="created"
        ) 