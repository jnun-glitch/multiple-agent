import os
import tempfile
from pathlib import Path
from backend.providers.local_hf import LocalHFProvider

class VoiceService:
    """Local Hugging Face STT/TTS service. No paid voice API required."""

    def __init__(self):
        self.provider=LocalHFProvider()

    async def transcribe(self,data:bytes,filename="recording.webm"):
        suffix=Path(filename).suffix or ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as f:
            f.write(data)
            path=f.name
        try:
            return await self.provider.transcribe(path)
        finally:
            Path(path).unlink(missing_ok=True)

    async def speech(self,text:str,voice_profile:str="calm"):
        return await self.provider.speech(text,voice_profile)
