# 🤗 Hugging Face Local Mode

<details><summary>💸 Kosten</summary>

Der Standardpfad nutzt lokale Modelle vom Hugging Face Hub. Nach dem Download werden LLM, STT und TTS auf deinem Rechner ausgeführt; es gibt keine laufende Inference-Abrechnung.

Hugging Face Inference Providers sind dagegen ein separater Cloud-Dienst mit begrenzten kostenlosen Credits.
</details>

<details><summary>🧠 Text-Modell</summary>

Standard: Qwen/Qwen2.5-1.5B-Instruct.

Für schwächere Hardware kannst du auf Qwen/Qwen2.5-0.5B-Instruct wechseln.
</details>

<details><summary>🎙️ Speech-to-Text</summary>

Standard: openai/whisper-tiny.

Whisper Tiny ist ein multilingualer 39M-Parameter-Checkpoint und kann deutsche Sprache lokal transkribieren.
</details>

<details><summary>🔊 Text-to-Speech</summary>

Standard: facebook/mms-tts-deu.

Das deutsche VITS-Modell ist ungefähr 291 MB groß und unter CC-BY-NC-4.0 veröffentlicht.

Die aktuelle Foundation nutzt ein deutsches Basis-Timbre und verschiedene Sprechprofile über die Geschwindigkeit. Wirklich unterschiedliche Stimmen werden später mit einem Multi-Speaker-Modell ergänzt.
</details>

<details><summary>⚙️ Modell wechseln</summary>

In .env:

```env
LOCAL_LLM_MODEL=Qwen/Qwen2.5-0.5B-Instruct
LOCAL_STT_MODEL=openai/whisper-tiny
LOCAL_TTS_MODEL=facebook/mms-tts-deu
DEVICE=auto
```

DEVICE=auto verwendet CUDA, wenn PyTorch eine kompatible NVIDIA-GPU erkennt, sonst CPU.
</details>

<details><summary>📦 Erster Start</summary>

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn backend.main:app --reload
```

Beim ersten Start werden die Modelle automatisch vom Hub geladen. Danach liegen sie im lokalen Hugging-Face-Cache.
</details>

<details><summary>🧪 Prüfen</summary>

```text
GET /api/health
```

Der Response sollte local-huggingface als Backend anzeigen.
</details>

## Modellquellen

- Qwen2.5 Instruct
- OpenAI Whisper
- Meta MMS German TTS
