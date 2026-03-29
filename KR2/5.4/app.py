from fastapi import FastAPI, Request, HTTPException
import re

app = FastAPI()

def is_valid_accept_language(value: str) -> bool:
    pattern = r"^[a-zA-Z]{2,3}(-[a-zA-Z]{2})?(, *[a-zA-Z]{2,3}(-[a-zA-Z]{2})?(;q=\d(\.\d)?)?)*$"
    return re.match(pattern, value) is not None

@app.get("/headers")
async def get_headers(request: Request):
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")

    if not user_agent or not accept_language:
        raise HTTPException(
            status_code=400,
            detail="Missing required headers"
        )

    if not is_valid_accept_language(accept_language):
        raise HTTPException(
            status_code=400,
            detail="Invalid Accept-Language format"
        )

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }