from sqlalchemy import Column, Integer, String
from .base import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, unique=True)
    grade = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
