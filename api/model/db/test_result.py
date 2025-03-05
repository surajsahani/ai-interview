from mongoengine import Document, StringField, IntField, FloatField, ListField, DictField
from datetime import datetime, UTC

class TestResult(Document):
    """Test result document model"""
    test_id = StringField(required=True, unique=True)
    user_id = StringField(required=True)
    summary = StringField(required=True)
    score = FloatField(required=True, min_value=0, max_value=100)
    question_number = IntField(required=True, min_value=0)
    correct_number = IntField(required=True, min_value=0)
    elapse_time = IntField(required=True, min_value=0)  # in seconds
    qa_history = ListField(DictField(), required=True)  # list of Q&A pairs
    
    meta = {
        'collection': 'ai_test_result',
        'indexes': [
            'test_id',
            'user_id',
            'score'
        ]
    } 