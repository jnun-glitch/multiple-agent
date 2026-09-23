from pathlib import Path
from fastapi import FastAPI,File,UploadFile,WebSocket,WebSocketDisconnect,HTTPException
from fastapi.responses import FileResponse,Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .core.events import EventBus
from .core.turn_lock import TurnManager
from .core.orchestrator import Orchestrator,load_agents
from .voice.service import VoiceService

bus=EventBus()
turns=TurnManager()
orchestrator=Orchestrator(load_agents(),bus,turns)
voice=VoiceService()

class SpeakRequest(BaseModel):
    text:str
    agent:str

class WSMgr:
    def __init__(self): self.clients=set()
    async def add(self,w): await w.accept(); self.clients.add(w)
    def remove(self,w): self.clients.discard(w)
    async def send(self,e):
        for w in list(self.clients):
            try: await w.send_json(e)
            except Exception: self.remove(w)

ws=WSMgr()
bus.subscribe(ws.send)
app=FastAPI(title="Multi-Agent Voice Lab")
front=Path(__file__).resolve().parent.parent/"frontend"
app.mount("/static",StaticFiles(directory=front),name="static")

@app.get("/")
async def index():
    return FileResponse(front/"index.html")

@app.get("/api/agents")
async def agents():
    return [{"id":a.id,"name":a.name,"role":a.role,"personality":a.personality,"voice":a.voice} for a in orchestrator.agents.values()]

@app.get("/api/health")
async def health():
    return {"ok":True,"turn_locked":turns.locked(),"speaker":turns.current_speaker}

@app.post("/api/transcribe")
async def transcribe(file:UploadFile=File(...)):
    data=await file.read()
    if not data: raise HTTPException(400,"Audio fehlt")
    return {"text":await voice.transcribe(data,file.filename or "recording.webm")}

@app.post("/api/chat")
async def chat(payload:dict):
    text=str(payload.get("text","")).strip()
    if not text: raise HTTPException(400,"Text fehlt")
    return await orchestrator.ask(text)

@app.post("/api/speak")
async def speak(payload:SpeakRequest):
    agent=orchestrator.agents.get(payload.agent)
    if not agent: raise HTTPException(404,"Agent fehlt")
    async with turns.speaking_turn(agent.id):
        await bus.publish({"type":"speaking_started","agent":agent.id,"name":agent.name})
        try:
            audio=await voice.speech(payload.text,agent.voice)
            return Response(audio,media_type="audio/mpeg")
        finally:
            await bus.publish({"type":"speaking_finished","agent":agent.id,"name":agent.name})

@app.websocket("/ws")
async def websocket(w:WebSocket):
    await ws.add(w)
    try:
        while True: await w.receive_text()
    except WebSocketDisconnect:
        ws.remove(w)
