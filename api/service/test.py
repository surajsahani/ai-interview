from api.model.test import CreateTestRequest, TestResponse

class TestService:
    async def create_test(self, request: CreateTestRequest) -> TestResponse:
        # 这里实现具体的业务逻辑
        return TestResponse(
            test_id=request.test_id,
            status="created"
        ) 