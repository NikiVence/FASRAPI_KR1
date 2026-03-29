from fastapi import FastAPI, Header, Depends, HTTPException, Response
from pydantic import BaseModel, field_validator
from typing import Annotated
import re
from datetime import datetime

app = FastAPI()

class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_language(cls, value):
        pattern = r"^[a-zA-Z]{2,3}(-[a-zA-Z]{2})?(, *[a-zA-Z]{2,3}(-[a-zA-Z]{2})?(;q=\d(\.\d)?)?)*$"
        if not re.match(pattern, value):
            raise ValueError("Invalid Accept-Language format")
        return value


def get_common_headers(
    user_agent: Annotated[str, Header(...)],
    accept_language: Annotated[str, Header(...)]
) -> CommonHeaders:
    try:
        return CommonHeaders(
            user_agent=user_agent,
            accept_language=accept_language
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/headers")
async def headers(headers: CommonHeaders = Depends(get_common_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def info(
    response: Response,
    headers: CommonHeaders = Depends(get_common_headers)
):
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()

    return {
        "message": "йо все чётко",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }