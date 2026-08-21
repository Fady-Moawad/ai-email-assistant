# 🤖 AI Email Assistant

An AI-powered REST API built with **FastAPI** and **Google Gemini API** for generating and analyzing emails.

The project demonstrates how to integrate an LLM into a Python backend application while using **Pydantic validation**, **structured JSON output**, and **token limit validation**.

---

## ⚙️ Installation & Running

```bash
pip install -r requirements.txt

---
## 🚀 Features


- ✉️ Generate professional emails using AI
- 🔍 Analyze existing emails
- 🧠 Google Gemini API integration
- 📦 Structured JSON output from Gemini
- ✅ Request validation using Pydantic
- 🔢 Token counting before analyzing emails
- 🚫 Maximum token limit protection
- 🏥 Health check endpoint
- 🔐 Environment variables for API configuration
- 🛣️ FastAPI Router-based project structure
- 📚 Automatic API documentation with Swagger UI

---

## 🛠️ Technologies

- **Python**
- **FastAPI**
- **Pydantic**
- **Google Gemini API**
- **Google GenAI Python SDK**
- **python-dotenv**
- **Uvicorn**

---

## 📁 Project Structure

```text
ai-email-assistant/
│
├── src/
│   └── routes/
│       └── ai_routes.py
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md