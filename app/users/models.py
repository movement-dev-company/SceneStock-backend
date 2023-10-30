from sqlalchemy import Boolean, Column, Integer, String

from . import schemas

# from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default=schemas.Role.USER)
    # is_staff = Column(Boolean, default=False)
    # disabled = Column(Boolean, default=False)
    # first_name = Column(String, nullable=True)
    # last_name = Column(String, nullable=True)
    # bio = Column(String, nullable=True)


class ConfirmationCode(Base):
    __tablename__ = 'confirmation_codes'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    confirmation_code = Column(String)
