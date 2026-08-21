from fastapi import FastAPI
from src.routes.ai_routes import router

app = FastAPI(
    title="AI Email Assistant",
    description="AI-powered email generation and analysis API",
    version="1.0.0"
)

app.include_router(router)