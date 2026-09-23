import tempfile
from pathlib import Path
from openai import AsyncOpenAI
from config.settings import TRANSCRIBE_MODEL,TTS_MODEL
class VoiceService:
 def __init__(self): self.client=AsyncOpenAI()
 async def transcribe(self,data,filename="recording.webm"):
  suffix=Path(filename).suffix or ".webm"
  with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as f: f.write(data); path=f.name
  try:
   with open(path,"rb") as audio: r=await self.client.audio.transcriptions.create(model=TRANSCRIBE_MODEL,file=audio)
   return r.text.strip()
  finally: Path(path).unlink(missing_ok=True)
 async def speech(self,text,voice):
  r=await self.client.audio.speech.create(model=TTS_MODEL,voice=voice,input=text,format="mp3")
  return r.content
