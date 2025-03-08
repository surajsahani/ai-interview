from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from api.model.api.base import Response
from api.model.api.question import CreateQuestionRequest, UpdateQuestionRequest, QuestionResponse
from api.service.question import QuestionService

router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Response[QuestionResponse])
async def create_question(request: CreateQuestionRequest):
    """
    创建新问题
    
    - **question**: 题目内容
    - **answer**: 答案内容
    - **examination_points**: 考查要点
    - **job_title**: 岗位名称
    - **language**: 语言
    - **difficulty**: 难度
    - **type**: 题目类型
    """
    service = QuestionService()
    question = await service.create_question(request)
    return Response[QuestionResponse](data=question)

@router.get("/{question_id}", response_model=Response[QuestionResponse])
async def get_question(question_id: str):
    """
    根据ID获取问题
    
    - **question_id**: 问题ID
    """
    service = QuestionService()
    question = await service.get_question(question_id)
    return Response[QuestionResponse](data=question)

@router.get("", response_model=Response[List[QuestionResponse]])
async def get_questions(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    获取问题列表（分页）
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = QuestionService()
    questions = await service.get_questions(skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.put("/{question_id}", response_model=Response[QuestionResponse])
async def update_question(question_id: str, request: UpdateQuestionRequest):
    """
    更新问题
    
    - **question_id**: 问题ID
    - **question**: 题目内容（可选）
    - **answer**: 答案内容（可选）
    - **examination_points**: 考查要点（可选）
    - **job_title**: 岗位名称（可选）
    - **language**: 语言（可选）
    - **difficulty**: 难度（可选）
    - **type**: 题目类型（可选）
    """
    service = QuestionService()
    question = await service.update_question(question_id, request)
    return Response[QuestionResponse](data=question)

@router.delete("/{question_id}", response_model=Response[dict])
async def delete_question(question_id: str):
    """
    删除问题
    
    - **question_id**: 问题ID
    """
    service = QuestionService()
    deleted = await service.delete_question(question_id)
    return Response[dict](data={"deleted": deleted})

@router.get("/search/{keyword}", response_model=Response[List[QuestionResponse]])
async def search_questions(
    keyword: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    搜索问题
    
    - **keyword**: 搜索关键词
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = QuestionService()
    questions = await service.search_questions(keyword, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/job/{job_title}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_job_title(
    job_title: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据岗位名称获取问题
    
    - **job_title**: 岗位名称
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = QuestionService()
    questions = await service.get_questions_by_job_title(job_title, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/difficulty/{difficulty}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_difficulty(
    difficulty: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据难度获取问题
    
    - **difficulty**: 难度
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = QuestionService()
    questions = await service.get_questions_by_difficulty(difficulty, skip, limit)
    return Response[List[QuestionResponse]](data=questions)

@router.get("/type/{type}", response_model=Response[List[QuestionResponse]])
async def get_questions_by_type(
    type: str,
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的最大记录数")
):
    """
    根据题目类型获取问题
    
    - **type**: 题目类型
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    """
    service = QuestionService()
    questions = await service.get_questions_by_type(type, skip, limit)
    return Response[List[QuestionResponse]](data=questions) 