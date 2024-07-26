from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy import Column, DateTime, Integer, String, Enum as EnumColumn, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from api.database import Base
from .user_schemas import UserRoles

has_all_user_access_roles = ['WORKFLOW', 'LAB', 'SERVICE_ADMIN']


def get_has_all_user_access(user_role):
    return user_role in has_all_user_access_roles


user_roles = list(UserRoles)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(EnumColumn(UserRoles, name='user_role_enum'), nullable=False)
    password_hash = Column(String(128), nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        try:
            return bcrypt.verify(password, self.password_hash)
        except Exception as e:
            raise HTTPException(401, str(e))

    @hybrid_property
    def has_all_user_access(self):
        return get_has_all_user_access(self.role)
