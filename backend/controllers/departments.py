from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services import department_service
from backend.utils.orm import serialize_list, serialize_model

router = APIRouter(prefix="/departments", tags=["departments"])


class DepartmentPayload(BaseModel):
    name: str
    description: str | None = None


class DepartmentUpdatePayload(BaseModel):
    name: str | None = None
    description: str | None = None


@router.get("", response_model=List[dict])
def list_departments():
    return serialize_list(department_service.list_departments())


@router.get("/{department_id}", response_model=dict)
def get_department(department_id: int):
    return serialize_model(department_service.get_department(department_id))


@router.post("", status_code=201, response_model=dict)
def create_department(payload: DepartmentPayload):
    return serialize_model(department_service.create_department(payload.dict()))


@router.put("/{department_id}", response_model=dict)
def update_department(department_id: int, payload: DepartmentUpdatePayload):
    return serialize_model(department_service.update_department(department_id, payload.dict(exclude_none=True)))


@router.delete("/{department_id}", status_code=200)
def delete_department(department_id: int):
    department_service.delete_department(department_id)
    return {"message": f"Department {department_id} deleted successfully"}
