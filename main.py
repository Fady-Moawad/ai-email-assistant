from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# like schema validation like struct in c++
class EmailRequest(BaseModel):
    title: str
    purpose: str
    tone: str = 'professional'
    recipient: str
    word_limit: int = 50

@app.get('/')
async def base():
    return {"message": "AI Email Assistant API"}

@app.post('/generate-email')
async def genEmail(data:EmailRequest):
    return {
        "title": data.title,
        "purpose": data.purpose,
        "tone": data.tone,
        "recipient": data.recipient,
        "word_limit": data.word_limit
    }