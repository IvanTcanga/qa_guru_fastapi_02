import uvicorn
from fastapi import FastAPI
from routers import status, users

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":


    uvicorn.run(app, host="localhost", port=8002)
