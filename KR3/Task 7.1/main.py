from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

security = HTTPBearer()


# фиктивные токены пользователей
fake_tokens = {
    "admin_token": {"username": "admin1", "role": "admin"},
    "user_token": {"username": "user1", "role": "user"},
    "guest_token": {"username": "guest1", "role": "guest"},
}


# роли и разрешения
roles = {
    "admin": ["create", "read", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"]
}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user = fake_tokens.get(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return user


def check_permission(permission: str):
    def checker(user=Depends(get_current_user)):
        user_role = user["role"]

        if permission not in roles[user_role]:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return checker


@app.get("/protected_resource")
def protected_resource(user=Depends(check_permission("read"))):
    return {"message": f"Hello {user['username']}"}


@app.post("/create_resource")
def create_resource(user=Depends(check_permission("create"))):
    return {"message": "Resource created"}


@app.put("/update_resource")
def update_resource(user=Depends(check_permission("update"))):
    return {"message": "Resource updated"}


@app.delete("/delete_resource")
def delete_resource(user=Depends(check_permission("delete"))):
    return {"message": "Resource deleted"}