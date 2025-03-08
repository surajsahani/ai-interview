from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.job import CreateJobRequest, UpdateJobRequest, JobResponse
from api.service.job import JobService

router = APIRouter(
    prefix="/job",
    tags=["job"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[JobResponse])
async def create_job(request: CreateJobRequest):
    """
    创建新职位
    
    - **job_title**: 职位名称
    - **job_description**: 职位描述
    - **technical_skills**: 技术技能要求
    - **soft_skills**: 软技能要求
    """
    service = JobService()
    job = await service.create_job(request)
    return Response[JobResponse](data=job)

@router.get("/{job_id}", response_model=Response[JobResponse])
async def get_job(job_id: str):
    """
    根据ID获取职位
    
    - **job_id**: 职位ID
    """
    service = JobService()
    job = await service.get_job(job_id)
    return Response[JobResponse](data=job)

@router.get("", response_model=Response[List[JobResponse]])
async def get_jobs(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    获取职位列表（分页）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = JobService()
    jobs = await service.get_jobs(skip, limit)
    return Response[List[JobResponse]](data=jobs)

@router.put("/{job_id}", response_model=Response[JobResponse])
async def update_job(job_id: str, request: UpdateJobRequest):
    """
    更新职位
    
    - **job_id**: 职位ID
    - **job_title**: 职位名称（可选）
    - **job_description**: 职位描述（可选）
    - **technical_skills**: 技术技能要求（可选）
    - **soft_skills**: 软技能要求（可选）
    """
    service = JobService()
    job = await service.update_job(job_id, request)
    return Response[JobResponse](data=job)

@router.delete("/{job_id}", response_model=Response[dict])
async def delete_job(job_id: str):
    """
    删除职位
    
    - **job_id**: 职位ID
    """
    service = JobService()
    deleted = await service.delete_job(job_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/search/{keyword}", response_model=Response[List[JobResponse]])
async def search_jobs(
    keyword: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    搜索职位
    
    - **keyword**: 搜索关键词
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = JobService()
    jobs = await service.search_jobs(keyword, skip, limit)
    return Response[List[JobResponse]](data=jobs) 