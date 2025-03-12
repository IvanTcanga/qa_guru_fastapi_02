import json
import uvicorn
from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from models import AppStatus
from models.User import User

app = FastAPI()

users: list[User] = []


# cлужебная ручка доступности сервиса
@app.get("/status", status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/user/{user_id}", status_code=HTTPStatus.OK)
# добавил типизацию прямо в аргументе функции
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    #id -> индекс списка (id-1)
    return users[user_id - 1]


@app.get("/api/users/", status_code=HTTPStatus.OK)
def get_users() -> list[User]:
    return users


if __name__ == "__main__":
    # Загрузить данные из файла JSON один раз при запуске сервера
    with open("users.json") as f:
        users = json.load(f)

    # методом pydantic model_validate проверить валидность данных из файла
    # валидны -возвращает None,  иначе исключение ValidationError
    # Это помогает обнаружить ошибки в данных на этапе загрузки, а не при обработке запросов
    for user in users:
        User.model_validate(user)

    print("Users loaded -> Server started")
    uvicorn.run(app, host="localhost", port=8002)