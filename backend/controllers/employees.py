from datetime import date
from typing import List, Optional
import os
from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr, validator
from backend.services import employee_service
from backend.utils.errors import BadRequestError
from backend.utils.orm import serialize_list, serialize_model

router = APIRouter(prefix="/employees", tags=["employees"])

TEST_FAILURE_HOOKS = os.getenv("ENABLE_TEST_FAILURE_HOOKS", "false").lower() == "true"


class EmployeePayload(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    hire_date: date
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = "active"

    @validator("status")
    def status_not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("status cannot be empty")
        return value.strip()


class EmployeeUpdatePayload(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    hire_date: Optional[date] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = None

    @validator("status")
    def status_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("status cannot be blank")
        return value.strip() if value is not None else value


def _split_full_name(full_name: str):
    if not full_name:
        return "", ""
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    return " ".join(parts[:-1]), parts[-1]


def _serialize_employee(emp):
    data = serialize_model(emp)
    if "full_name" in data:
        first_name, last_name = _split_full_name(data.pop("full_name"))
        data["first_name"] = first_name
        data["last_name"] = last_name
    return data


@router.get("", response_model=List[dict])
def list_employees():
    employees = employee_service.list_employees()
    return [_serialize_employee(emp) for emp in employees]


@router.get("/with-payroll", response_model=List[dict])
def list_employees_with_payroll():
    combined = []
    pairs = employee_service.list_employees_with_payroll()
    for emp, salary in pairs:
        emp_data = _serialize_employee(emp)
        emp_data["latest_salary"] = serialize_model(salary) if salary is not None else None
        combined.append(emp_data)
    return combined


@router.get("/{employee_id}", response_model=dict)
def get_employee(employee_id: int):
    return serialize_model(employee_service.get_employee(employee_id))


@router.post("", status_code=201, response_model=dict)
def create_employee(payload: EmployeePayload, request: Request):
    simulate_mysql_failure = TEST_FAILURE_HOOKS and request.headers.get("x-simulate-mysql-failure", "false").lower() == "true"
    employee = employee_service.create_employee(payload.dict(), simulate_mysql_failure=simulate_mysql_failure)
    # service may return either a serialized dict (already safe) or a SQLAlchemy model
    if isinstance(employee, dict):
        return employee
    return serialize_model(employee)


@router.put("/{employee_id}", response_model=dict)
def update_employee(employee_id: int, payload: EmployeeUpdatePayload, request: Request):
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise BadRequestError("At least one field must be provided for update")
    simulate_mysql_failure = TEST_FAILURE_HOOKS and request.headers.get("x-simulate-mysql-failure", "false").lower() == "true"
    updated = employee_service.update_employee(employee_id, update_data, simulate_mysql_failure=simulate_mysql_failure)
    if isinstance(updated, dict):
        return updated
    return serialize_model(updated)


@router.delete("/{employee_id}", status_code=200)
def delete_employee(employee_id: int):
    employee_service.delete_employee(employee_id)
    return {"message": f"Employee {employee_id} deleted successfully"}
