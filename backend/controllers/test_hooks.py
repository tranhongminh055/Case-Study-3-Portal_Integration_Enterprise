import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.session import SessionSqlServer, SessionMysql
from backend.models.salary import Salary
from backend.models.dividend import Dividend
from backend.models.employee import Employee
from backend.models.department import Department
from backend.models.position import Position
from backend.utils.orm import serialize_model
from backend.utils.errors import NotFoundError

router = APIRouter(prefix="/testing", tags=["testing"])


def verify_test_hooks_enabled():
    if os.getenv("ENABLE_TEST_FAILURE_HOOKS", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Test hooks are disabled")


class SalaryPayload(BaseModel):
    employee_id: int
    amount: float
    effective_date: str


class DividendPayload(BaseModel):
    employee_id: int
    amount: float
    paid_date: str


@router.post("/mysql/salary", status_code=201)
def setup_mysql_salary(payload: SalaryPayload):
    verify_test_hooks_enabled()
    with SessionMysql() as session:
        salary = Salary(**payload.dict())
        session.add(salary)
        session.commit()
        return serialize_model(salary)


@router.post("/sql/dividend", status_code=201)
def setup_sql_dividend(payload: DividendPayload):
    verify_test_hooks_enabled()
    with SessionSqlServer() as session:
        dividend = Dividend(**payload.dict())
        session.add(dividend)
        session.commit()
        return serialize_model(dividend)


@router.get("/mysql/employee/{employee_id}", response_model=dict)
def get_mysql_employee(employee_id: int):
    verify_test_hooks_enabled()
    with SessionMysql() as session:
        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise NotFoundError(f"MySQL employee {employee_id} not found")
        return serialize_model(employee)


@router.get("/mysql/department/{department_id}", response_model=dict)
def get_mysql_department(department_id: int):
    verify_test_hooks_enabled()
    with SessionMysql() as session:
        department = session.query(Department).filter(Department.id == department_id).first()
        if not department:
            raise NotFoundError(f"MySQL department {department_id} not found")
        return serialize_model(department)


@router.get("/mysql/position/{position_id}", response_model=dict)
def get_mysql_position(position_id: int):
    verify_test_hooks_enabled()
    with SessionMysql() as session:
        position = session.query(Position).filter(Position.id == position_id).first()
        if not position:
            raise NotFoundError(f"MySQL position {position_id} not found")
        return serialize_model(position)
