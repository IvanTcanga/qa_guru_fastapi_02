
from pydantic import BaseModel


# модель статуса работы сервиса,говорящая о статусе загружены ли данные users в БД на основке флага
class AppStatus(BaseModel):
    users: bool
