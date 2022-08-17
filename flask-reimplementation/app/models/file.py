from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField
from datetime import datetime

class File(Document):
    file_id = IntField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    s3_path = StringField(required=True)
    file_extension = StringField(required=True)
    file_name = StringField(required=True)
    
    