from mongoengine import Document, StringField

class User(Document):
    """User document model"""
    user_id = StringField(required=True, unique=True)
    user_name = StringField(required=True)
    
    meta = {
        'collection': 'ai_user',
        'indexes': ['user_id']
    } 