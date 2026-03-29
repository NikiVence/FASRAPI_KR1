from fastapi import FastAPI, HTTPException, Response, Request
from itsdangerous import URLSafeSerializer, BadSignature
import uuid
import time

app = FastAPI()

SECRET_KEY = "SUPER_SECRET_KEY"
serializer = URLSafeSerializer(SECRET_KEY)

SESSION_LIFETIME = 300
REFRESH_THRESHOLD = 180

users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com"
    }
}

def create_session_token(user_id: str, timestamp: int):
    data = f"{user_id}.{timestamp}"
    signature = serializer.dumps(data)
    return signature

def verify_session_token(token: str):
    try:
        data = serializer.loads(token)
        user_id, timestamp = data.split(".")
        return user_id, int(timestamp)
    except (BadSignature, ValueError):
        return None, None

@app.post("/login")
async def login(response: Response, username: str, password: str):
    user = users_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    current_time = int(time.time())

    token = create_session_token(user_id, current_time)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,
        max_age=SESSION_LIFETIME
    )

    return {"message": "Login successful"}

@app.get("/profile")
async def profile(request: Request, response: Response):
    token = request.cookies.get("session_token")

    if not token:
        response.status_code = 401
        return {"message": "Session expired"}

    user_id, last_activity = verify_session_token(token)

    if not user_id:
        response.status_code = 401
        return {"message": "Invalid session"}

    current_time = int(time.time())
    elapsed = current_time - last_activity

    if elapsed > SESSION_LIFETIME:
        response.status_code = 401
        return {"message": "Session expired"}

    if REFRESH_THRESHOLD <= elapsed <= SESSION_LIFETIME:
        new_token = create_session_token(user_id, current_time)

        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=SESSION_LIFETIME
        )

    return {
        "user_id": user_id,
        "last_activity": last_activity,
        "message": "Active session"
    }