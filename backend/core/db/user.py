from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField
from datetime import datetime
from core.db.workspace import Workspace
from core.db.job import Job
from flask_bcrypt import generate_password_hash, check_password_hash

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(max_length=128)
    last_name = StringField(max_length=128)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    workspaces = ListField(ReferenceField(Workspace), default=[])
    jobs = ListField(ReferenceField(Job), default=[])
    
    
    def hash_password(self) -> None:
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, test_password) -> bool:
        return check_password_hash(self.password, test_password)


    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs)
