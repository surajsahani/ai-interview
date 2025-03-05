from typing import Optional, List
from loguru import logger
from api.model.db.job import Job
from api.utils.log_decorator import log

class JobRepository:
    @log
    async def create_job(self, job: Job) -> Job:
        """Create a new job"""
        return job.save()
    
    @log
    async def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return Job.objects(job_id=job_id).first()
    
    @log
    async def get_jobs_by_title(self, title: str) -> List[Job]:
        """Get jobs by title"""
        return Job.objects(job_title__icontains=title).all()
    
    @log
    async def update_job(self, job: Job) -> Job:
        """Update job"""
        return job.save()
    
    @log
    async def delete_job(self, job_id: str) -> bool:
        """Delete job by ID"""
        result = Job.objects(job_id=job_id).delete()
        return result > 0 