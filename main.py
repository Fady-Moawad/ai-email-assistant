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

class EmailResponse(BaseModel):
    subject: str
    greeting: str
    body: str
    closing: str

class AnalyzeEmailRequest(BaseModel):
    email: str = Field(min_length=10)

class AnalyzeEmailResponse(BaseModel):
    summary: str
    key_information: list[str]
    action_items: list[str]

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
            contents=prompt,
            config={
                'response_mime_type':'application/json',
                'response_schema':EmailResponse
                }
        )

        return {
            "success": True,
            # return stractured data insted of text
            "email": response.parsed
            # return text of string until if you try to ask from gemini to return stractured data
            # "email": response.parsed
        }

    except Exception:
       raise HTTPException ( 
            status_code=500,
            detail="Failed to generate email")

@app.post('/analyze-email')          
async def analyze_email(data:AnalyzeEmailRequest):
    try:
        prompt = f"""
Analyze the following email:

{data.email}

Extract the following information:

- A short summary
- Key information
- Action items

Return the result using the required structured format.
"""
        response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema":AnalyzeEmailResponse
        }
    )
        return {
            "success": True,
            "analysis": response.parsed
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