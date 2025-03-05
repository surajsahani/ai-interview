from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class TestType(str, Enum):
    CODING = "coding"
    SYSTEM_DESIGN = "system_design"
    BEHAVIOR = "behavior"

class TestLanguage(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"

class TestDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class CreateTestRequest(BaseModel):
    test_id: str
    type: TestType
    language: TestLanguage
    difficulty: TestDifficulty
    create_date: datetime

class TestResponse(BaseModel):
    test_id: str
    status: str = "created" 