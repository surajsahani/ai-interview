from mongoengine import Document, StringField, ListField

class Job(Document):
    """Job document model"""

    # Job id, e.g. '1234567890'
    job_id = StringField(required=True, unique=True)

    # Job title, e.g. React Developer, Java Developer, etc.
    job_title = StringField(required=True)

    # Job description, e.g. Java API Developer, etc.
    job_description = StringField(required=True)
    
    # Required skills for the job, e.g. ['React', 'JavaScript', 'CSS']
    technical_skills = ListField(StringField(), required=True)

    # Required soft skills for the job, e.g. ['Communication', 'Teamwork', 'Problem-solving']
    soft_skills = ListField(StringField(), required=True)
    
    meta = {
        'collection': 'ai_job',
        'indexes': [
            'job_id',
            'job_title',
            'job_skills'
        ]
    } 