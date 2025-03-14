from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from app.database import users_db
from app.models.User import User
from fastapi_pagination import Page, add_pagination, paginate


router = APIRouter(prefix="/api/user")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be > 0")
    if user_id > len(users_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users_db[user_id - 1]


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users_db)


