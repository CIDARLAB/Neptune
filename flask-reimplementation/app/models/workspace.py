from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField, IntField
from datetime import datetime
from app.models.file import File

from app.models.job import Job

class Workspace(Document):
    workspace_id = IntField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    jobs = ListField(ReferenceField(Job), default=[])
    design_files = ListField(ReferenceField(File), default=[])
    solution_files = ListField(ReferenceField(File), default=[])
    other_files = ListField(ReferenceField(File), default=[])
