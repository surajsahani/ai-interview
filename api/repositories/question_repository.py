from typing import List
from api.model.db.question import Question
from api.utils.log_decorator import log

class QuestionRepository:
    @log
    async def create_question(self, question: Question) -> Question:
        """Create a new question"""
        return question.save()
    
    @log
    async def get_questions_by_job(self, job_title: str, language: str) -> List[Question]:
        """Get questions for a specific job and language"""
        return Question.objects(job_title=job_title, language=language).all()
    
    @log
    async def get_questions_by_knowledge_point(self, knowledge_point: str) -> List[Question]:
        """Get questions by knowledge point"""
        return Question.objects(knowledge_points=knowledge_point).all() 