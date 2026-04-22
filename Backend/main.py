# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat")
async def chat(request: ChatRequest):

    # Build full message list with system prompt
    full_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + request.messages

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=full_messages,
        max_tokens=500,       # keep responses concise
        temperature=0.7       # some creativity but not too random
    )

    return {
        "response": response.choices[0].message.content
    }

@app.get("/")
async def root():
    return {"status": "running"}