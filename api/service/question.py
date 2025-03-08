import uuid
from typing import List, Optional
from api.model.api.question import CreateQuestionRequest, UpdateQuestionRequest, QuestionResponse
from api.model.db.question import Question
from api.repositories.question_repository import QuestionRepository
from api.utils.log_decorator import log
from api.exceptions.api_error import NotFoundError, DuplicateError

class QuestionService:
    def __init__(self):
        self.repository = QuestionRepository()
    
    @log
    async def create_question(self, request: CreateQuestionRequest) -> QuestionResponse:
        """创建新问题"""
        # 创建问题文档
        question = Question(
            question_id=str(uuid.uuid4()),
            question=request.question,
            answer=request.answer,
            examination_points=request.examination_points,
            job_title=request.job_title,
            language=request.language,
            difficulty=request.difficulty,
            type=request.type
        )
        
        # 保存到数据库
        question = await self.repository.create_question(question)
        
        return self._to_response(question)
    
    @log
    async def get_question(self, question_id: str) -> QuestionResponse:
        """根据ID获取问题"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("问题不存在")
        
        return self._to_response(question)
    
    @log
    async def get_questions(self, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """获取问题列表（分页）"""
        questions = await self.repository.get_questions(skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def update_question(self, question_id: str, request: UpdateQuestionRequest) -> QuestionResponse:
        """更新问题"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("问题不存在")
        
        # 更新提供的字段
        if request.question is not None:
            question.question = request.question
        if request.answer is not None:
            question.answer = request.answer
        if request.examination_points is not None:
            question.examination_points = request.examination_points
        if request.job_title is not None:
            question.job_title = request.job_title
        if request.language is not None:
            question.language = request.language
        if request.difficulty is not None:
            question.difficulty = request.difficulty
        if request.type is not None:
            question.type = request.type
        
        question = await self.repository.update_question(question)
        return self._to_response(question)
    
    @log
    async def delete_question(self, question_id: str) -> bool:
        """删除问题"""
        question = await self.repository.get_question_by_id(question_id)
        if not question:
            raise NotFoundError("问题不存在")
        
        return await self.repository.delete_question(question_id)
    
    @log
    async def search_questions(self, keyword: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """搜索问题"""
        questions = await self.repository.search_questions(keyword, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_job_title(self, job_title: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """根据岗位名称获取问题"""
        questions = await self.repository.get_questions_by_job_title(job_title, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_examination_points(self, examination_points: List[str], skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """根据考查要点获取问题"""
        questions = await self.repository.get_questions_by_examination_points(examination_points, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_difficulty(self, difficulty: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """根据难度获取问题"""
        questions = await self.repository.get_questions_by_difficulty(difficulty, skip, limit)
        return [self._to_response(question) for question in questions]
    
    @log
    async def get_questions_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[QuestionResponse]:
        """根据题目类型获取问题"""
        questions = await self.repository.get_questions_by_type(type, skip, limit)
        return [self._to_response(question) for question in questions]
    
    def _to_response(self, question: Question) -> QuestionResponse:
        """将Question文档转换为QuestionResponse"""
        return QuestionResponse(
            question_id=question.question_id,
            question=question.question,
            answer=question.answer,
            examination_points=question.examination_points,
            job_title=question.job_title,
            language=question.language,
            difficulty=question.difficulty,
            type=question.type
        ) 