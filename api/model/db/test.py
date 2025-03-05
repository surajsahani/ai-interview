from mongoengine import Document, StringField, DateTimeField, IntField
from datetime import datetime, UTC

class Test(Document):
    """Test document model"""
    # Test identification
    test_id = StringField(required=True, unique=True)
    activate_code = StringField(required=True, unique=True)
    
    # User information
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    
    # Job information
    job_id = StringField(required=True)
    job_title = StringField(required=True)
    job_description = StringField(required=True)
    
    # Test configuration
    type = StringField(required=True, choices=['coding', 'system_design', 'behavior'])
    language = StringField(required=True, choices=['python', 'java', 'javascript'])
    difficulty = StringField(required=True, choices=['easy', 'medium', 'hard'])
    test_time = IntField(required=True, min_value=15, max_value=120)  # minutes
    
    # Test status
    status = StringField(
        required=True, 
        choices=['open', 'on-going', 'completed'],
        default='open'
    )
    
    # Timestamps
    create_date = DateTimeField(default=lambda: datetime.now(UTC))
    start_date = DateTimeField()
    close_date = DateTimeField()
    
    meta = {
        'collection': 'ai_test',
        'indexes': [
            'test_id',
            'activate_code',
            'user_id',
            'job_id',
            ('type', 'language', 'difficulty'),
            'status',
            'create_date'
        ]
    } 