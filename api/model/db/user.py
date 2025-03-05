from mongoengine import Document, StringField, IntField, DateTimeField, EmailField
from datetime import datetime, UTC

class User(Document):
    """User document model"""
    user_id = StringField(required=True, unique=True)
    user_name = StringField(required=True)
    password = StringField(required=True)  # Should be hashed before saving
    staff_id = StringField()
    email = EmailField(required=True, unique=True)
    status = IntField(required=True, choices=[0, 1], default=0)  # 0:active, 1:inactive
    role = IntField(required=True, choices=[0, 1], default=1)    # 0:interviewer, 1:interviewee
    create_date = DateTimeField(default=lambda: datetime.now(UTC))
    
    meta = {
        'collection': 'ai_user',
        'indexes': [
            'user_id',
            'email',
            'staff_id',
            ('status', 'role')
        ]
    } 