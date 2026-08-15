from fastapi import FastAPI
from pydantic import BaseModel , Field
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# like schema validation like struct in c++
class EmailRequest(BaseModel):
    title: str = Field(min_length=3)
    purpose: str
    tone: str = Field(default='professional') 
    recipient: str
    word_limit: int = Field(default=50, ge=20, le=500)

@app.get('/')
async def base():
    return {"message": "AI Email Assistant API"}

@app.post('/generate-email')
async def genEmail(data:EmailRequest):
    prompt = f"""
    Write an email based on the following requirements:

    Title: {data.title}
    Purpose: {data.purpose}
    Tone: {data.tone}
    Recipient: {data.recipient}
    Word limit: {data.word_limit}

    Return only the email.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return {
        "success": True,
        "email": response.text
    }

@app.get('/test')
async def test():
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Write a short professional email asking for vacation."
    )
    return {
        "response": response.text
    }