from pydantic import BaseModel

class User(BaseModel):
    age: int
    name: str