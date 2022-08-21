from uuid import uuid4
from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField
from datetime import datetime

class File(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    s3_path = StringField(required=True)
    file_extension = StringField(required=True)
    file_name = StringField(required=True)
    
    def save(self, *args, **kwargs):
        if self.file_name is None:
            raise ValueError("File name is required")
        self.modified_date = datetime.now()
        if self.file_name is not None:
            self.file_extension = self.file_name.split('.')[-1]
        return super(File, self).save(*args, **kwargs)
    