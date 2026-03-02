from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post("/user")
async def root(user: User):    
    return {
        "user": user,
        "is_adult": user.age >= 18
    }
    