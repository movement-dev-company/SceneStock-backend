import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class Role(str, Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class BaseUser(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

    @validator('email')
    def validate_email_length(cls, value):
        if len(value) > 256:
            raise ValueError("Email length must not exceed 256 characters")
        return value

    @validator('password')
    def validate_password(cls, value):
        errors = []
        if len(value) <= 8:
            errors.append(
                'Password must be at least 8 characters long'
            )
        if not re.search('[a-z]', value):
            errors.append(
                'Password must contain at least one lowercase letter'
            )
        if not re.search('[A-Z]', value):
            errors.append(
                'Password must contain at least one uppercase letter'
            )
        if not re.search('[0-9]', value):
            errors.append(
                'Password must contain at least one number'
            )
        if not re.search('[-_!.]', value):
            errors.append(
                'Password must contain at least one special character'
            )
        if errors:
            raise ValueError(errors)
        return value


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    role: Optional[Role] = Field(default=Role.USER)

    class Config:
        orm_mode = True


class ConfirmationCode(BaseUser):
    confirmation_code: str = Field(
        min_length=6, max_length=6, regex=r'^[0-9]{6}$'
    )


class LoginUser(BaseModel):
    email: EmailStr
    password: str
