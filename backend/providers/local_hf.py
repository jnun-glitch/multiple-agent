import asyncio
import io
import threading

import numpy as np
import soundfile as sf
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    VitsModel,
    VitsTokenizer,
)

from config.settings import (
    DEVICE,
    LOCAL_LLM_MODEL,
    LOCAL_STT_MODEL,
    LOCAL_TTS_MODEL,
    MAX_NEW_TOKENS,
)

class LocalHFProvider:
    """Local-only Hugging Face inference for chat, STT and German TTS."""

    def __init__(self):
        self._lock=threading.Lock()
        self._tokenizer=None
        self._llm=None
        self._stt=None
        self._tts_model=None
        self._tts_tokenizer=None

    def _device(self):
        if DEVICE == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return DEVICE

    def _ensure_llm(self):
        if self._llm is not None: return
        with self._lock:
            if self._llm is not None: return
            self._tokenizer=AutoTokenizer.from_pretrained(LOCAL_LLM_MODEL)
            kwargs={}
            if self._device()=="cuda":
                kwargs.update(device_map="auto",torch_dtype=torch.float16)
            else:
                kwargs.update(torch_dtype=torch.float32)
            self._llm=AutoModelForCausalLM.from_pretrained(LOCAL_LLM_MODEL,**kwargs)

    def _ensure_stt(self):
        if self._stt is not None: return
        with self._lock:
            if self._stt is not None: return
            device=0 if self._device()=="cuda" else -1
            self._stt=pipeline(
                "automatic-speech-recognition",
                model=LOCAL_STT_MODEL,
                device=device,
            )

    def _ensure_tts(self):
        if self._tts_model is not None: return
        with self._lock:
            if self._tts_model is not None: return
            device=self._device()
            self._tts_tokenizer=VitsTokenizer.from_pretrained(LOCAL_TTS_MODEL)
            self._tts_model=VitsModel.from_pretrained(LOCAL_TTS_MODEL)
            self._tts_model.to(device)
            self._tts_model.eval()

    def _chat_sync(self,messages):
        self._ensure_llm()
        inputs=self._tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
        )
        inputs=inputs.to(self._llm.device)
        with torch.no_grad():
            out=self._llm.generate(
                inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.08,
            )
        generated=out[0][inputs.shape[-1]:]
        return self._tokenizer.decode(generated,skip_special_tokens=True).strip()

    async def chat(self,messages):
        return await asyncio.to_thread(self._chat_sync,messages)

    def _transcribe_sync(self,path):
        self._ensure_stt()
        result=self._stt(path,generate_kwargs={"language":"german","task":"transcribe"})
        return result["text"].strip()

    async def transcribe(self,path):
        return await asyncio.to_thread(self._transcribe_sync,path)

    def _tts_sync(self,text,profile):
        self._ensure_tts()
        device=self._device()
        inputs=self._tts_tokenizer(text,return_tensors="pt").to(device)
        with torch.no_grad():
            waveform=self._tts_model(**inputs).waveform.squeeze().detach().cpu().numpy()
        rate=float(self._tts_model.config.sampling_rate)
        speed={"fast":1.07,"bright":1.03,"calm":0.98,"slow":0.94}.get(profile,1.0)
        if speed != 1.0 and len(waveform)>1:
            new_len=max(2,int(len(waveform)/speed))
            x_old=np.linspace(0.0,1.0,num=len(waveform))
            x_new=np.linspace(0.0,1.0,num=new_len)
            waveform=np.interp(x_new,x_old,waveform).astype(np.float32)
        buf=io.BytesIO()
        sf.write(buf,waveform,rate,format="WAV",subtype="PCM_16")
        return buf.getvalue()

    async def speech(self,text,profile):
        return await asyncio.to_thread(self._tts_sync,text,profile)
