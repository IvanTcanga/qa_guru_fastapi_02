# Микросервис управления пользователями

Микросервис на базе FastAPI для управления данными пользователей с автоматизированными тестами.

## Описание

Этот микросервис предоставляет REST API для получения информации о пользователях. Поддерживает пагинацию и включает в себя тестовое покрытие.

## Возможности

- Получение списка всех пользователей с пагинацией
- Получение пользователя по ID
- Эндпоинт статуса для проверки работоспособности сервиса
- Валидация входных данных с использованием Pydantic моделей
- Комплексный набор тестов

## API Эндпоинты

### GET /status/

Возвращает текущий статус сервиса.

Ответ:

```json
{
  "users": true
}
```

### GET /api/users/

Возвращает постраничный список всех пользователей.

Ответ:

```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "avatar": "https://example.com/avatar.jpg"
    }
  ],
  "total": 10,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### GET /api/users/{user_id}

Возвращает конкретного пользователя по ID.

Ответ:

```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "https://example.com/avatar.jpg"
}
```

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Скопируйте `.env.sample` в `.env` и настройте:

```bash
cp .env.sample .env
```

5. Запустите сервис:

```bash
python main.py
```

Сервис запустится по адресу, указанному в переменной APP_URL .env-файла.

## Тестирование

Проект включает различные наборы тестов:

### Смоук тесты (Smoke Tests)

- Базовая проверка работоспособности сервиса
- Доступность эндпоинта пользователей
- Получение случайного пользователя

### Тесты пользователей

- Получение всех пользователей
- Проверка на отсутствие дубликатов ID пользователей
- Получение конкретных пользователей по ID
- Тестирование несуществующих ID пользователей
- Тестирование некорректных форматов ID пользователей

Для запуска тестов:

```bash
pytest tests/
```

Для запуска определенных категорий тестов:

```bash
pytest -m "smoke"  # Запуск smoke тестов
pytest -m "users_tests"  # Запуск тестов пользователей
pytest -m "pagination"  # Запуск тестов пагинации
pytest -m "not smoke" # Запуск всех тестов, кроме smoke
```

## Модели данных

### Модель пользователя (User)

```python
class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl
```

### Модель статуса приложения (AppStatus)

```python
class AppStatus(BaseModel):
    users: bool
```

## Обработка ошибок

Сервис включает обработку следующих ошибок:

- Некорректные ID пользователей (400 Bad Request)
- Несуществующие пользователи (404 Not Found)
- Некорректные форматы входных данных (422 Unprocessable Entity)
