from fastapi import FastAPI
from models import Feedback

app = FastAPI()

reviews = []

@app.post("/feedback")
async def root(feedback: Feedback):    
    reviews.append(feedback)
    return {"message": f"Feedback received. Thank you, {feedback.name}."}
    