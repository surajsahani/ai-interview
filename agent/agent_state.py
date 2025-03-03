from typing import (
    Annotated,
    Sequence,
    TypedDict,
)
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from agent.interview_response import AnalyzeAnswerResponse, Question
from enum import Enum
from datetime import datetime

class Language(str, Enum):
    ENGLISH = "English"
    CHINESE = "Chinese"

class AgentState(TypedDict):
    """The state of the agent."""
    start_time: datetime

    # chat history (for user interaction and display)
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # interview requirement
    job_title: str
    knowledge_points: str
    interview_time: int = 3
    language: Language = Language.ENGLISH

    # current user answer and feedback
    question: Question | None = None
    user_answer: str | None = None
    analyze_answer_response: AnalyzeAnswerResponse | None = None
    
