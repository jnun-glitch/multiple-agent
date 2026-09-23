import os
from dotenv import load_dotenv
load_dotenv()

LOCAL_LLM_MODEL=os.getenv("LOCAL_LLM_MODEL","Qwen/Qwen2.5-1.5B-Instruct")
LOCAL_STT_MODEL=os.getenv("LOCAL_STT_MODEL","openai/whisper-tiny")
LOCAL_TTS_MODEL=os.getenv("LOCAL_TTS_MODEL","facebook/mms-tts-deu")
MAX_NEW_TOKENS=int(os.getenv("MAX_NEW_TOKENS","384"))
DEVICE=os.getenv("DEVICE","auto")
HOST=os.getenv("HOST","127.0.0.1")
PORT=int(os.getenv("PORT","8000"))
