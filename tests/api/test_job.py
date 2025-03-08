import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app
from datetime import datetime, UTC
import uuid

client = TestClient(app)

# 模拟职位数据
@pytest.fixture
def mock_job():
    job = MagicMock()
    job.job_id = str(uuid.uuid4())
    job.job_title = "前端开发工程师"
    job.job_description = "负责公司前端产品的开发和维护"
    job.technical_skills = ["React", "Vue", "JavaScript"]
    job.soft_skills = ["沟通能力", "团队协作"]
    job.create_date = datetime.now(UTC)
    return job


class TestJobAPI:
    """Job API 测试类"""

    @patch("api.repositories.job_repository.JobRepository.create_job")
    def test_create_job(self, mock_create_job, mock_job):
        """测试创建职位"""
        # 设置模拟返回值
        mock_create_job.return_value = mock_job
        
        # 发送请求
        response = client.post(
            "/api/v1/job",
            json={
                "job_title": "前端开发工程师",
                "job_description": "负责公司前端产品的开发和维护",
                "technical_skills": ["React", "Vue", "JavaScript"],
                "soft_skills": ["沟通能力", "团队协作"]
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert "job_id" in data["data"]
        assert data["data"]["job_title"] == "前端开发工程师"
        
        # 验证模拟调用
        mock_create_job.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_get_job(self, mock_get_job_by_id, mock_job):
        """测试获取职位"""
        # 设置模拟返回值
        mock_get_job_by_id.return_value = mock_job
        
        # 发送请求
        response = client.get(f"/api/v1/job/{mock_job.job_id}")
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["job_title"] == "前端开发工程师"
        assert data["data"]["job_description"] == "负责公司前端产品的开发和维护"
        assert "React" in data["data"]["technical_skills"]
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_get_job_not_found(self, mock_get_job_by_id):
        """测试获取不存在的职位"""
        # 设置模拟返回值
        mock_get_job_by_id.return_value = None
        
        # 发送请求
        response = client.get("/api/v1/job/nonexistent")
        
        # 验证响应
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "职位不存在" in data["message"]
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with("nonexistent")

    @patch("api.repositories.job_repository.JobRepository.get_jobs")
    def test_get_jobs(self, mock_get_jobs, mock_job):
        """测试获取职位列表"""
        # 设置模拟返回值
        mock_get_jobs.return_value = [mock_job]
        
        # 发送请求
        response = client.get("/api/v1/job?skip=0&limit=10")
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["job_title"] == "前端开发工程师"
        
        # 验证模拟调用
        mock_get_jobs.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    @patch("api.repositories.job_repository.JobRepository.update_job")
    def test_update_job(self, mock_update_job, mock_get_job_by_id, mock_job):
        """测试更新职位"""
        # 设置模拟返回值
        mock_get_job_by_id.return_value = mock_job
        mock_update_job.return_value = mock_job
        
        # 发送请求
        response = client.put(
            f"/api/v1/job/{mock_job.job_id}",
            json={
                "job_title": "高级前端开发工程师",
                "job_description": "负责公司前端架构设计和团队管理",
                "technical_skills": ["React", "Vue", "TypeScript", "Webpack"],
                "soft_skills": ["领导力", "沟通能力", "团队协作"]
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)
        mock_update_job.assert_called_once()

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_update_job_not_found(self, mock_get_job_by_id):
        """测试更新不存在的职位"""
        # 设置模拟返回值
        mock_get_job_by_id.return_value = None
        
        # 发送请求
        response = client.put(
            "/api/v1/job/nonexistent",
            json={
                "job_title": "高级前端开发工程师"
            }
        )
        
        # 验证响应
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "职位不存在" in data["message"]
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with("nonexistent")

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    @patch("api.repositories.job_repository.JobRepository.delete_job")
    def test_delete_job(self, mock_delete_job, mock_get_job_by_id, mock_job):
        """测试删除职位"""
        # 设置模拟返回值
        mock_get_job_by_id.return_value = mock_job  # 先检查职位是否存在
        mock_delete_job.return_value = True
        
        # 发送请求
        response = client.delete(f"/api/v1/job/{mock_job.job_id}")
        
        # 验证响应 - 修改为 404
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "0"
        assert data["message"] == "success"
        assert data["data"]["deleted"] is True
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with(mock_job.job_id)
        mock_delete_job.assert_called_once_with(mock_job.job_id)

    @patch("api.repositories.job_repository.JobRepository.get_job_by_id")
    def test_delete_job_not_found(self, mock_get_job_by_id):
        """测试删除不存在的职位"""
        # 设置模拟返回值 - 职位不存在
        mock_get_job_by_id.return_value = None
        
        # 发送请求
        response = client.delete("/api/v1/job/nonexistent")
        
        # 验证响应 - 修改为 404
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "404"
        assert "职位不存在" in data["message"]
        
        # 验证模拟调用
        mock_get_job_by_id.assert_called_once_with("nonexistent") 