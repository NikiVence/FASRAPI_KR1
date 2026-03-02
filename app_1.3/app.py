from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Calc(BaseModel):
    n1: int
    n2: int

@app.post("/calculate")
async def root(item: Calc):
    return {"result": item.n1 + item.n2}