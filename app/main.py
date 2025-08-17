from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

from app.config import settings
from app.memory import memory
from app.prompts import make_system_prompt

app = FastAPI(title="Chatbot API")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    temperature: float = 0.3
    top_p: float = 0.9

class ChatResponse(BaseModel):
    reply: str

async def call_ollama(messages, temperature: float, top_p: float) -> str:
    payload = {
        "model": settings.model_name,
        "messages": messages,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
        },
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{settings.ollama_host}/v1/chat/completions", json=payload)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Ollama error: {r.text}")
        data = r.json()
        # OpenAI-compatible return format
        return data["choices"][0]["message"]["content"].strip()

@app.get("/")
async def root():
    return {"ok": True, "model": settings.model_name}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # Build chat history: system + previous + user
    sys = {"role": "system", "content": make_system_prompt(settings.system_prompt)}
    history = [sys] + memory.get(req.session_id) + [{"role": "user", "content": req.message}]

    reply = await call_ollama(history, req.temperature, req.top_p)

    # Save turns
    memory.add(req.session_id, "user", req.message)
    memory.add(req.session_id, "assistant", reply)
    memory.truncate(req.session_id)

    return ChatResponse(reply=reply)
