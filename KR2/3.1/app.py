from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
import re

app = FastAPI()
arr = []
class UserCreate(BaseModel):
    name: str = Field(..., description="name")
    email: str = Field(..., description="email")
    age: int = Field(..., description="age")
    is_subscribed: bool = Field(..., description="is_subscribed")

    @validator('email')
    def email_validator(cls, v: str) -> str:
        EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        if not EMAIL_RE.match(v):
            raise ValueError('invalid email')
        return v

@app.post("/create_user")
def create_user(user: UserCreate):
    arr.append(user)
    return {"message": "User created successfully", "user": user}
        