from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from api.model.api.base import Response
from api.model.api.chat import StartChatRequest, AnswerRequest, ChatResponse
from api.service.chat import ChatService
from api.utils.log_decorator import log
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

router = APIRouter(prefix="/chat", tags=["Chat"])

# 服务实例
chat_service = ChatService()

@router.post("/start", response_model=Response[ChatResponse])
@log
async def start_chat(request: StartChatRequest):
    """
    开始聊天
    
    开始一个新的面试聊天会话，返回第一个问题
    """
    try:
        # 调用服务层方法
        result = await chat_service.start_chat(
            user_id=request.user_id,
            test_id=request.test_id,
            job_title=request.job_title,
            examination_points=request.examination_points,
            test_time=request.test_time,
            language=request.language,
            difficulty=request.difficulty
        )
        
        # 返回成功响应
        return Response[ChatResponse](
            code="0",
            message="success",
            data=result
        )
    except Exception as e:
        # 处理异常
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/answer", response_model=Response[ChatResponse])
@log
async def answer_question(request: AnswerRequest):
    """
    回答问题
    
    提交用户对问题的回答，获取下一个问题或反馈
    """
    try:
        # 调用服务层方法
        result = await chat_service.process_answer(
            user_id=request.user_id,
            test_id=request.test_id,
            question_id=request.question_id,
            user_answer=request.user_answer
        )
        
        # 返回成功响应
        return Response[ChatResponse](
            code="0",
            message="success",
            data=result
        )
    except Exception as e:
        # 处理异常
        raise HTTPException(status_code=500, detail=str(e))