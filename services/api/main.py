from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import redis
import json
import asyncio

app = FastAPI()

# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

clients = []

class Event(BaseModel):
    service: str
    metric: str
    value: float
    severity: str


# 📥 Event ingestion
@app.post("/event")
def ingest_event(event: Event):
    r.lpush("event_queue", json.dumps(event.dict()))
    return {"status": "queued"}


# 🖥 Dashboard
@app.get("/")
def home():
    with open("services/api/dashboard.html") as f:
        return HTMLResponse(f.read())


# 🔴 Live WebSocket stream
@app.websocket("/live")
async def live_feed(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(ws)


async def broadcast(message: str):
    for ws in clients:
        await ws.send_text(message)


# 📡 Push updates from worker
@app.post("/push")
async def push_update(data: dict):
    await broadcast(str(data))
    return {"ok": True}