from fastapi import FastAPI, HTTPException
from models import Feedback

app = FastAPI()

reviews = []

@app.post("/feedback")
async def root(feedback: Feedback):
    try:
        feedback_entry = {
            "name": feedback.name,
            "message": feedback.message
        }
        reviews.append(feedback_entry)
        
        return {
            "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении: {str(e)}")
    