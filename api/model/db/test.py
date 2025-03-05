from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Test(Document):
    """Test document model"""
    test_id = StringField(required=True, unique=True)
    type = StringField(required=True, choices=['coding', 'system_design', 'behavior'])
    language = StringField(required=True, choices=['python', 'java', 'javascript'])
    difficulty = StringField(required=True, choices=['easy', 'medium', 'hard'])
    create_date = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'ai_test',
        'indexes': [
            'test_id',
            ('type', 'language', 'difficulty')
        ]
    } 