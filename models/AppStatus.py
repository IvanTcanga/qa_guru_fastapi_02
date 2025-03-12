
from pydantic import BaseModel


# модель статуса работы сервиса сообщающая есть ли данные users в БД на основке флага
class AppStatus(BaseModel):
    users: bool
