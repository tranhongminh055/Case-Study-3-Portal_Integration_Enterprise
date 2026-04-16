from typing import List
from fastapi import APIRouter
from backend.services import payroll_service
from backend.utils.orm import serialize_list

router = APIRouter(tags=["payroll"])


@router.get("/salaries", response_model=List[dict])
def get_salaries():
    return serialize_list(payroll_service.list_salaries())


@router.get("/attendance", response_model=List[dict])
def get_attendance():
    return serialize_list(payroll_service.list_attendance())
