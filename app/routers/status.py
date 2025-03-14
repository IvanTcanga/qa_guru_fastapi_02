from http import HTTPStatus
from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database import users_db

router = APIRouter()


# cлужебная ручка доступности сервиса
@router.get("/status", status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(users=bool(users_db))
