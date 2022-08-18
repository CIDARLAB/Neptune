from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField, ListField, ReferenceField

from datetime import datetime
from app.models.file import File

class Job(Document):
    job_id = IntField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    files = ListField(ReferenceField(File), default=[])