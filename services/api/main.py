from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

class Event(BaseModel):
    service: str
    metric: str
    value: float
    severity: str

@app.post("/event")
def ingest_event(event: Event):
    r.lpush("event_queue", json.dumps(event.dict()))
    return {"status": "queued"}


from fastapi import WebSocket
import asyncio

clients = []

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