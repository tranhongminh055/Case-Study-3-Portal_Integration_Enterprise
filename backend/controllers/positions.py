from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services import position_service
from backend.utils.orm import serialize_list, serialize_model

router = APIRouter(prefix="/positions", tags=["positions"])


class PositionPayload(BaseModel):
    title: str
    grade: str | None = None
    description: str | None = None


class PositionUpdatePayload(BaseModel):
    title: str | None = None
    grade: str | None = None
    description: str | None = None


@router.get("", response_model=List[dict])
def list_positions():
    return serialize_list(position_service.list_positions())


@router.get("/{position_id}", response_model=dict)
def get_position(position_id: int):
    return serialize_model(position_service.get_position(position_id))


@router.post("", status_code=201, response_model=dict)
def create_position(payload: PositionPayload):
    return serialize_model(position_service.create_position(payload.dict()))


@router.put("/{position_id}", response_model=dict)
def update_position(position_id: int, payload: PositionUpdatePayload):
    return serialize_model(position_service.update_position(position_id, payload.dict(exclude_none=True)))


@router.delete("/{position_id}", status_code=200)
def delete_position(position_id: int):
    position_service.delete_position(position_id)
    return {"message": f"Position {position_id} deleted successfully"}
