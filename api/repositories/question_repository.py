from typing import Optional, List
from api.model.db.question import Question
from api.utils.log_decorator import log

class QuestionRepository:
    @log
    async def create_question(self, question: Question) -> Question:
        """创建新问题"""
        return question.save()
    
    @log
    async def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """根据ID获取问题"""
        return Question.objects(question_id=question_id).first()
    
    @log
    async def get_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """获取问题列表（分页）"""
        return Question.objects().skip(skip).limit(limit).all()
    
    @log
    async def update_question(self, question: Question) -> Question:
        """更新问题"""
        return question.save()
    
    @log
    async def delete_question(self, question_id: str) -> bool:
        """删除问题"""
        result = Question.objects(question_id=question_id).delete()
        return result > 0
    
    @log
    async def search_questions(self, keyword: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """搜索问题"""
        return Question.objects(
            question__icontains=keyword
        ).skip(skip).limit(limit).all()
    
    @log
    async def get_questions_by_job_title(self, job_title: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """根据岗位名称获取问题"""
        return Question.objects(
            job_title=job_title
        ).skip(skip).limit(limit).all()
    
    @log
    async def get_questions_by_examination_points(self, examination_points: List[str], skip: int = 0, limit: int = 100) -> List[Question]:
        """根据考查要点获取问题"""
        return Question.objects(
            examination_points__in=examination_points
        ).skip(skip).limit(limit).all()
    
    @log
    async def get_questions_by_difficulty(self, difficulty: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """根据难度获取问题"""
        return Question.objects(
            difficulty=difficulty
        ).skip(skip).limit(limit).all()
    
    @log
    async def get_questions_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """根据题目类型获取问题"""
        return Question.objects(
            type=type
        ).skip(skip).limit(limit).all()

    @log
    async def get_questions_by_job(self, job_title: str, language: str) -> List[Question]:
        """Get questions for a specific job and language"""
        return Question.objects(job_title=job_title, language=language).all()
    
    @log
    async def get_questions_by_knowledge_point(self, knowledge_point: str) -> List[Question]:
        """Get questions by knowledge point"""
        return Question.objects(knowledge_points=knowledge_point).all() 