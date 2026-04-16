from sqlalchemy import Column, Integer, Numeric, Date
from .base import Base

class Dividend(Base):
    __tablename__ = "dividends"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    paid_date = Column(Date, nullable=False)
