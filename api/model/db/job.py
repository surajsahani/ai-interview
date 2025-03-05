from mongoengine import Document, StringField

class Job(Document):
    """Job document model"""
    job_id = StringField(required=True, unique=True)
    job_title = StringField(required=True)
    job_description = StringField(required=True)
    
    meta = {
        'collection': 'ai_job',
        'indexes': [
            'job_id',
            'job_title'
        ]
    } 