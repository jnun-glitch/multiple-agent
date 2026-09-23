# 🎙️ Voice

<details><summary>Aktuelle Pipeline</summary>
Mikrofon → Browser MediaRecorder → `/api/transcribe` → STT → Orchestrator → Agent → `/api/speak` → TTS → Browser.
</details>
<details><summary>Anti-Overlap</summary>
TTS-Aufrufe müssen durch den zentralen `TurnManager` laufen. Dadurch wartet ein zweiter Sprecher.
</details>
<details><summary>Nächster Ausbau</summary>
Realtime/STT-Streaming, VAD, Interrupt/Resume, Audio-Queue und echte Sprecherzustände.
</details>
