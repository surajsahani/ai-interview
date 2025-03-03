from enum import Enum
from pydantic import BaseModel, Field

class QuestionType(str, Enum):
    SINGLE_CHOICE = "Single Choice"
    MULTIPLE_CHOICE = "Multiple Choice"
    ESSAY = "Essay"
    SHORT_ANSWER = "Short Answer"
    TRUE_FALSE = "True False"


class Question(BaseModel):
    question: str = Field(description="The question of the interview, including choices")
    question_number: int = Field(description="The number of the question, start from 1")
    question_type: QuestionType = Field(description="The type of the question")
    knowledge_point: str = Field(description="The knowledge point of the question")
    answer: str = Field(description="The answer of the question")


class AnalyzeAnswerResponse(BaseModel):
  
    is_answer: bool = Field(description="Whether the answer is a valid answer to the previous question")
    feedback: str = Field(description="The feedback of the answer to the previous question")
    is_correct: bool = Field(description="Whether the answer is correct to the previous question")
    answer_analysis: str = Field(description="The analysis of the answer to the previous question")
    answer_score: int = Field(description="The score of the answer to the previous question (0-5)")

    is_interview_over: bool = Field(description="Whether the interview is over")

    next_question: Question | None = Field(description="Generate a new question for the interview")


class Answer(BaseModel):
    is_valid: bool = Field(description="Whether the answer is a valid response")
    feedback: str = Field(description="Friendly feedback of the answer")
    is_correct: bool = Field(description="Whether the answer is correct")
    analysis: str = Field(description="The analysis of the answer")
    score: int = Field(description="The score of the answer (0-5)")


class QAResult(BaseModel):
    question: Question = Field(description="The question of the interview")
    answer: Answer = Field(description="The answer of the question")
    is_interview_over: bool = Field(description="Whether the interview is over")
    

