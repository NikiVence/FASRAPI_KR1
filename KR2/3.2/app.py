from fastapi import FastAPI, HTTPException, Response, Request
import uuid

app = FastAPI()

# ---------------------------
# 👤 "База пользователей"
# ---------------------------
users_db = {
    "user123": {
        "username": "user123",
        "password": "password123",
        "email": "user123@example.com"
    }
}

# ---------------------------
# 🧠 Хранилище сессий
# ---------------------------
sessions = {}

# ---------------------------
# 🔑 LOGIN
# ---------------------------
@app.post("/login")
async def login(response: Response, username: str, password: str):
    user = users_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # создаём токен
    session_token = str(uuid.uuid4())

    # сохраняем сессию
    sessions[session_token] = username

    # устанавливаем cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False  
    )

    return {"message": "Login successful"}


@app.get("/user")
async def get_user(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token or session_token not in sessions:
        raise HTTPException(
            status_code=401,
            detail={"message": "Unauthorized"}
        )

    username = sessions[session_token]
    user = users_db[username]

    return {
        "username": user["username"],
        "email": user["email"]
    }