import os
from dotenv import load_dotenv
load_dotenv()
CHAT_MODEL=os.getenv("CHAT_MODEL","gpt-5.6-luna")
TRANSCRIBE_MODEL=os.getenv("TRANSCRIBE_MODEL","gpt-4o-transcribe")
TTS_MODEL=os.getenv("TTS_MODEL","gpt-4o-mini-tts")
HOST=os.getenv("HOST","127.0.0.1")
PORT=int(os.getenv("PORT","8000"))
