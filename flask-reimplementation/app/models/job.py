from uuid import uuid4
from mongoengine import Document, StringField, IntField, DateTimeField, ListField, ReferenceField

from datetime import datetime
from app.models.file import File

class Job(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    files = ListField(ReferenceField(File), default=[])
    status = StringField(default='pending')
    task_meta_refernce = StringField(default='')

    def save(self, *args, **kwargs):
        self.modified_date = datetime.now()
        return super(Job, self).save(*args, **kwargs)
