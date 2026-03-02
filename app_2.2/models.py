from pydantic import BaseModel, Field, validator


class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="name от 2 до 50 символов")
    message: str = Field(..., min_length=10, max_length=500, description="message от 10 до 500 символов")

    @validator("message")
    def valid_m(cls, v):
        v_lower = v.lower()
        BANNED_WORDS = ["кринж", "рофл", "вайб"]

        for word in BANNED_WORDS:
            if word in v_lower:
                raise ValueError('Использование недопустимых слов')
        
        return v
