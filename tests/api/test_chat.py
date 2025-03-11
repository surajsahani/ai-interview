import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app
import uuid

client = TestClient(app)

class TestChatAPI:
    """Chat API 测试类"""

    @patch("api.service.chat.ChatService.start_chat")
    def test_start_chat(self, mock_start_chat):
        """测试开始聊天"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        
        # 设置模拟返回值
        mock_response = {
            "feedback": "请介绍一下你的 Python 编程经验",
            "question_id": str(uuid.uuid4()),
            "type": "question"
        }
        mock_start_chat.return_value = mock_response
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/start",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "job_title": "Python 开发工程师",
                "examination_points": "Python, Django, Flask",
                "test_time": 60,
                "language": "Chinese",
                "difficulty": "medium"
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["feedback"] == mock_response["feedback"]
        assert data["data"]["question_id"] == mock_response["question_id"]
        assert data["data"]["type"] == "question"
        
        # 验证模拟调用
        mock_start_chat.assert_called_once()
        args, kwargs = mock_start_chat.call_args
        assert kwargs["user_id"] == user_id
        assert kwargs["test_id"] == test_id
        assert kwargs["job_title"] == "Python 开发工程师"
        assert kwargs["examination_points"] == "Python, Django, Flask"
        assert kwargs["test_time"] == 60
        assert kwargs["language"] == "Chinese"
        assert kwargs["difficulty"] == "medium"

    @patch("api.service.chat.ChatService.process_answer")
    def test_process_answer(self, mock_process_answer):
        """测试处理回答"""
        # 准备测试数据
        test_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        question_id = str(uuid.uuid4())
        user_answer = "我有5年的Python开发经验，主要使用Django和Flask框架..."
        
        # 设置模拟返回值
        mock_response = {
            "feedback": "很好的回答。下一个问题：请描述一下你使用过的设计模式",
            "question_id": str(uuid.uuid4()),
            "type": "question"
        }
        mock_process_answer.return_value = mock_response
        
        # 发送请求
        response = client.post(
            "/api/v1/chat/answer",
            json={
                "user_id": user_id,
                "test_id": test_id,
                "question_id": question_id,
                "user_answer": user_answer
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["feedback"] == mock_response["feedback"]
        assert data["data"]["question_id"] == mock_response["question_id"]
        assert data["data"]["type"] == "question"
        
        # 验证模拟调用
        mock_process_answer.assert_called_once_with(
            user_id=user_id,
            test_id=test_id,
            question_id=question_id,
            user_answer=user_answer
        ) 