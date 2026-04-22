import os
import secrets

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "DEV")
DOCS_USER = os.getenv("DOCS_USER", "admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "123")

if MODE not in ["DEV", "PROD"]:
    raise ValueError("MODE must be DEV or PROD")


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


fake_users_db = {}


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user = fake_users_db.get(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

    correct_username = secrets.compare_digest(username, user.username)
    correct_password = pwd_context.verify(password, user.hashed_password)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

    return user


def check_docs_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, DOCS_USER)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)

    if not (correct_user and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.post("/register")
def register(user: User):
    hashed_password = pwd_context.hash(user.password)

    user_in_db = UserInDB(
        username=user.username,
        hashed_password=hashed_password
    )

    fake_users_db[user.username] = user_in_db

    return {"message": "User added successfully"}


@app.get("/login")
def login(current_user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {current_user.username}!"}


if MODE == "DEV":

    @app.get("/docs", include_in_schema=False, dependencies=[Depends(check_docs_auth)])
    def custom_docs():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="docs"
        )


    @app.get("/openapi.json", include_in_schema=False, dependencies=[Depends(check_docs_auth)])
    def openapi():
        return JSONResponse(app.openapi())