from fastapi import APIRouter
from backend.services import report_service

router = APIRouter(tags=["reports"])


@router.get("/reports", response_model=list)
def get_reports():
    return report_service.get_reports()
