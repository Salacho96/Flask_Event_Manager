from todor.extensions import db
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    ATTENDEE = "attendee"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.ATTENDEE, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(password.encode(), self.password_hash)

    @staticmethod
    def hash_password(password: str) -> bytes:
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())