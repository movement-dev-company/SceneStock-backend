from sqlalchemy import Column, Integer, String

from core.database import Base


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    slug = Column(String, unique=True, index=True)
