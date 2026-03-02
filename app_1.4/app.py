from fastapi import FastAPI
from models import User

niki = User(id=1, name="NIKI")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

@app.get("/users")
async def get_user():
    return niki