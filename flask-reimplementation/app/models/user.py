from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField
from datetime import datetime
from app.models.workspace import Workspace
from app.models.job import Job

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    workspaces = ListField(ReferenceField(Workspace), default=[])
    jobs = ListField(ReferenceField(Job), default=[])