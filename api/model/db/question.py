from mongoengine import Document, StringField, ListField

class Question(Document):
    """Question document model"""
    question = StringField(required=True)
    answer = StringField(required=True)
    knowledge_points = ListField(StringField(), required=True)
    job_title = StringField(required=True)
    language = StringField(required=True, choices=['python', 'java', 'javascript'])
    
    meta = {
        'collection': 'ai_question',
        'indexes': [
            ('job_title', 'language'),
            'knowledge_points'
        ]
    } 