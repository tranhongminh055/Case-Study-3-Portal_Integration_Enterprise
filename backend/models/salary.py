from sqlalchemy import Column, Integer, Numeric, Date
from .base import Base

class Salary(Base):
    __tablename__ = "salaries"

    id = Column("SalaryID", Integer, primary_key=True, index=True)
    employee_id = Column("EmployeeID", Integer, nullable=False, index=True)
    base_salary = Column("BaseSalary", Numeric(12, 2), nullable=False)
    bonus = Column("Bonus", Numeric(12, 2), nullable=True)
    deductions = Column("Deductions", Numeric(12, 2), nullable=True)
    amount = Column("NetSalary", Numeric(12, 2), nullable=False)
    effective_date = Column("SalaryMonth", Date, nullable=False)
