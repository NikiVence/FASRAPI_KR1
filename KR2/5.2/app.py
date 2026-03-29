from fastapi import FastAPI, HTTPException, Response, Request
from itsdangerous import URLSafeSerializer, BadSignature
import uuid

app = FastAPI()


SECRET_KEY = "SUPER_SECRET_KEY"

serializer = URLSafeSerializer(SECRET_KEY)

users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com"
    }
}

@app.post("/login")
async def login(response: Response, username: str, password: str):
    user = users_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # создаём user_id (UUID)
    user_id = str(uuid.uuid4())

    signed_token = serializer.dumps(user_id)

    response.set_cookie(
        key="session_token",
        value=signed_token,
        httponly=True,
        max_age=3600
    )

    return {"message": "Login successful"}

@app.get("/profile")
async def profile(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    try:
        user_id = serializer.loads(session_token)
    except BadSignature:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    return {
        "user_id": user_id,
        "message": "Authorized"
    }