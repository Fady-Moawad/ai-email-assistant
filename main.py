from fastapi import FastAPI,HTTPException
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
    word_limit: int = Field(default=50, ge=20, le=100)

@app.get('/')
async def base():
    return {"message": "AI Email Assistant API"}

@app.post('/generate-email')
async def genEmail(data: EmailRequest):
    # AI call must in error boundary
    try:
        # Structured Output With Prompt
        prompt = f"""
Write an email based on the following requirements:

Title: {data.title}
Purpose: {data.purpose}
Tone: {data.tone}
Recipient: {data.recipient}
Word limit: {data.word_limit}

Return the result as JSON with exactly these fields:

{{
    "subject": "...",
    "greeting": "...",
    "body": "...",
    "closing": "..."
}}

Do not add any other fields.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return {
            "success": True,
            "email": response.text
        }

    except Exception:
       raise HTTPException ( 
            status_code=500,
            detail="Failed to generate email")

            
        
@app.get('/test')
async def test():
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Write a short professional email asking for vacation."
    )
    return {
        "response": response.text
    }