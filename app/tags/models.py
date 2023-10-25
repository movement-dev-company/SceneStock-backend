from sqlalchemy import Column, Integer, String

# from sqlalchemy.orm import relationship
from core.database import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    slug = Column(String, unique=True, index=True)
