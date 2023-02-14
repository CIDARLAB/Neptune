from uuid import uuid4
from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField, IntField
from datetime import datetime
from fluigi_cloud.db.file import File

from fluigi_cloud.db.job import Job

class Workspace(Document):
    name = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    jobs = ListField(ReferenceField(Job), default=[])
    design_files = ListField(ReferenceField(File), default=[])
    solution_files = ListField(ReferenceField(File), default=[])
    other_files = ListField(ReferenceField(File), default=[])


    def save(self, *args, **kwargs):
        self.modified_date = datetime.now()
        return super(Workspace, self).save(*args, **kwargs)
