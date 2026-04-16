from sqlalchemy import Column, Integer, String, Date
from .base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    work_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    leave_hours = Column(Integer, nullable=False, default=0)
