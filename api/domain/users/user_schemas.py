from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    email: str
    role: str

    created_at: datetime
    updated_at: datetime


class UserCredentialsSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: str

    class Config:
        from_attributes = True


class UserRoles(Enum):
    CUSTOMER_CLIENT = 'CUSTOMER_CLIENT'
    WORKFLOW = 'WORKFLOW'
    LAB = 'LAB'
    SERVICE_ADMIN = 'SERVICE_ADMIN'


class UserCreationRequestSchema(BaseModel):
    email: str
    password: str
    role: UserRoles


class UserUpdateSchema(BaseModel):
    role: Optional[UserRoles] = None
    password: Optional[str] = None
