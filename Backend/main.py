# backend/main.py

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq, APIError
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not set — add it to Backend/.env")

app = FastAPI(title="Personal Finance Assistant")
client = Groq(api_key=api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

SYSTEM_PROMPT = """
You are a friendly personal finance assistant.

Your job is to help users understand their finances,
build better habits, and make smarter decisions.

HOW TO BEHAVE:
- If the user hasn't mentioned their income yet,
  ask for it naturally — don't interrogate them,
  just work it into the conversation
- Keep responses concise and conversational
- Always end with one specific actionable tip
  or a follow up question to learn more about them
- Use simple language, avoid jargon
- If they seem stressed about money, acknowledge
  that first before jumping into numbers

WHAT YOU KNOW:
- Budgeting frameworks (50/30/20, zero based, etc.)
- Saving strategies
- Debt management (avalanche vs snowball)
- Basic investment concepts
- Emergency fund importance

IMPORTANT:
- Never give specific stock or crypto advice
- Always add a disclaimer for investment topics
- You are not a licensed financial advisor
"""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.post("/chat")
async def chat(request: ChatRequest):
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        m.model_dump() for m in request.messages
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=full_messages,
            max_tokens=500,
            temperature=0.7,
        )
    except APIError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {e.message}")

    return {"response": response.choices[0].message.content}


@app.get("/")
async def root():
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
