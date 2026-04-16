from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from .base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column("EmployeeID", Integer, primary_key=True, index=True)
    full_name = Column("FullName", String(200), nullable=False)
    date_of_birth = Column("DateOfBirth", Date, nullable=True)
    gender = Column("Gender", String(50), nullable=True)
    phone = Column("PhoneNumber", String(50), nullable=True)
    email = Column("Email", String(200), nullable=False, unique=True)
    hire_date = Column("HireDate", Date, nullable=False)
    department_id = Column("DepartmentID", Integer, ForeignKey("departments.id"), nullable=True)
    position_id = Column("PositionID", Integer, ForeignKey("positions.id"), nullable=True)
    status = Column("Status", String(50), nullable=False, default="active")
    created_at = Column("CreatedAt", DateTime, nullable=True)
    updated_at = Column("UpdatedAt", DateTime, nullable=True)
