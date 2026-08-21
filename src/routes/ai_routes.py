from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from google import genai
from typing import Literal
from dotenv import load_dotenv
import os


load_dotenv()

router = APIRouter()

MAXIMUM_TOKEN = int(os.getenv("MAXIMUM_TOKEN"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class EmailRequest(BaseModel):
    title: str = Field(min_length=3)
    purpose: str
    tone: Literal["formal", "friendly", "professional"] = "professional"
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


@router.get("/")
async def base():
    return {"message": "AI Email Assistant API"}


@router.post("/generate-email")
async def generate_email(data: EmailRequest):
    try:
        prompt = f"""
Write an email based on the following requirements:

Title: {data.title}
Purpose: {data.purpose}
Tone: {data.tone}
Recipient: {data.recipient}
Word limit: {data.word_limit}

Return the result using the required structured format.
"""

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": EmailResponse
            }
        )

        return {
            "success": True,
            "email": response.parsed
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate email"
        )


@router.post("/analyze-email")
async def analyze_email(data: AnalyzeEmailRequest):
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

        count_token = client.models.count_tokens(
            model=os.getenv("MODEL"),
            contents=prompt
        )

        if count_token.total_tokens > MAXIMUM_TOKEN:
            raise HTTPException(
                status_code=413,
                detail="Email is too long to analyze"
            )

        response = client.models.generate_content(
            model=os.getenv("MODEL"),
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": AnalyzeEmailResponse
            }
        )

        return {
            "success": True,
            "analysis": response.parsed
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze email"
        )


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "AI Email Assistant"
    }