from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField, ListField, ReferenceField

from datetime import datetime
from app.models.file import File
from app.models.user import User
from app.models.workspace import Workspace

class Job(Document):
    job_id = IntField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    workspace = ReferenceField(Workspace)
    user = ReferenceField(User)
    files = ListField(ReferenceField(File), default=[])