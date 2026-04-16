from fastapi import APIRouter
from backend.services import alert_service
from backend.utils.logger import logger


router = APIRouter(tags=["alerts"])


@router.get("/alerts", response_model=dict)
def get_alerts():
    try:
        return alert_service.get_alerts()
    except Exception as e:
        logger.exception("Alert service failed: %s", e)
        # return empty structure so frontend can still render
        return {"anniversaries": [], "abnormal_salaries": [], "excessive_leave": []}
