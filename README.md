# 🤖 MULTI-AGENT VOICE LAB

> Ein modulares Multi-Agent-System: mehrere Persönlichkeiten, Voice, Agent↔Agent-Kommunikation und ein zentraler Turn-Lock – mit klaren Erweiterungspunkten für Coding, Vision, Dateien, Web und weitere Tools.

## 🧭 Navigation
<details><summary>✨ Features</summary>

**Core:** Orchestrator, Rollen, Persönlichkeiten, Memory, Event Bus, Turn-Lock und Team-Kommunikation.

**Voice:** Browser-Mikrofon → STT → Agent-Auswahl → Antwort → TTS.

**UI:** Live-Agent-Status, Sprecheranzeige, Chat und Voice-Aufnahme.

**Future-ready:** getrennte ToolRegistry/Skills, Coding-/Vision-Schnittstellen, Dokumente, Web-Research, persistent Memory und Streaming als klare nächste Schichten.
</details>

<details><summary>🏗️ Architektur</summary>

```text
                         USER
                          │
                 ┌────────▼────────┐
                 │  WEB FRONTEND   │
                 │ Chat / Mic / UI │
                 └───────┬─────────┘
                         │ HTTP / WS
                ┌────────▼─────────┐
                │   ORCHESTRATOR   │
                │ route / delegate │
                └───┬──────┬──────┘
                    │      │
              ┌─────▼─┐ ┌─▼──────┐
              │ AGENTS │ │ TOOLS  │
              │persona │ │ skills  │
              └───┬────┘ └────┬───┘
                  │             │
                  └──────┬──────┘
                         ▼
                    EVENT BUS
                         │
                         ▼
                    TURN LOCK
                         │
                         ▼
                        TTS
                         │
                         ▼
                    USER AUDIO
```
</details>

<details><summary>🔒 Turn-Lock – warum die Agenten sich nicht stören</summary>

Der Turn-Lock ist zentral und unabhängig von der Persönlichkeit. Jeder Audio-Turn muss durch `TurnManager.speaking_turn()`.

```text
Alex       THINK ─────► SPEAK 🔒 ─────► DONE
Nova       THINK ─────► WAIT  💤 ──────► SPEAK
Mira       THINK ─────► WAIT  💤
```

**Wichtig:** Interne Agent-Events erzeugen nicht automatisch Audio. Das verhindert, dass drei Agenten gleichzeitig sprechen.
</details>

<details><summary>🎙️ Voice</summary>

```text
Microphone
  ↓
MediaRecorder
  ↓
/api/transcribe
  ↓
Speech-to-Text
  ↓
Orchestrator
  ↓
Selected Agent
  ↓
Turn-Lock
  ↓
Text-to-Speech
  ↓
Browser Audio
```
</details>

<details><summary>🤖 Agenten & Persönlichkeiten</summary>

| Agent | Rolle | Charakter |
|---|---|---|
| Alex | Coding / Technik | direkt, technisch, lösungsorientiert |
| Nova | Research | analytisch, vorsichtig, präzise |
| Mira | Creative | kreativ, freundlich, ideenreich |
| Iris | Vision | visuell, strukturiert, erklärend |
| Atlas | Supervisor | plant, delegiert, prüft |

Agenten sind Konfiguration + Code, nicht fest in der UI verdrahtet.
</details>

<details><summary>💬 Agent ↔ Agent</summary>

Agenten kommunizieren über interne Events. Später kann der Supervisor einen echten Task-Graphen bauen:

```text
User Task
  ↓
Atlas
  ├──► Nova: Recherche
  ├──► Alex: Implementierung
  └──► Iris: Bildanalyse
          ↓
     Result Merger
          ↓
       Finalizer
```

Nur der ausgewählte finale Sprecher erzeugt User-Audio.
</details>

<details><summary>🧰 Zukunft: Coding / Bild / Dateien / Web</summary>

Die Architektur trennt Agenten von Tools. Geplante Skills:

- `coding` – Workspace, Diff, Tests, Linting
- `vision` – Bilder verstehen und visuelle Aufgaben
- `image_generation` – Bilder erzeugen
- `files` – Dateien/Dokumente lesen und schreiben
- `web_research` – Recherche und Quellen
- `python` – kontrollierte Berechnungen
- `browser` – spätere Browser-Automation

Damit muss man für einen neuen Skill nicht den ganzen Orchestrator umbauen.
</details>

<details><summary>💾 Memory</summary>

Es gibt eine austauschbare Memory-Schicht. Kurzzeitkontext wird lokal gehalten; später können SQLite, Vektorsuche, Sessions und selektives Long-Term-Memory dahinter gesetzt werden.
</details>

<details><summary>⚙️ Setup</summary>

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Linux/macOS:
```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
</details>

<details><summary>▶️ Start</summary>

```bash
python -m uvicorn backend.main:app --reload
```

Dann: `http://127.0.0.1:8000`
</details>

<details><summary>🧪 Tests</summary>

```bash
pytest
```
</details>

<details><summary>📁 Projektstruktur</summary>

```text
backend/
  agents/       Personas
  core/         Orchestrator, Memory, Events, Turn-Lock
  tools/        Skills / Tool Registry
  voice/        STT / TTS
frontend/       Web UI
config/         Agent-Konfiguration
docs/            klickbare Detail-Dokumentation
tests/           Tests
.github/         CI
```
</details>

## 📚 Dokumentation
- [🏗️ Architektur](docs/ARCHITECTURE.md)
- [🤖 Agenten](docs/AGENTS.md)
- [🎙️ Voice](docs/VOICE.md)
- [💾 Memory](docs/MEMORY.md)
- [🧰 Tools & Skills](docs/TOOLS.md)
- [👨‍💻 Coding](docs/CODING.md)
- [🖼️ Vision](docs/VISION.md)
- [📁 Files](docs/FILES.md)
- [🌐 Research](docs/RESEARCH.md)
- [🔐 Security](docs/SECURITY.md)
- [🧩 Extending](docs/EXTENDING.md)
- [🗺️ Roadmap](docs/ROADMAP.md)
- [⚠️ Known Issues](docs/KNOWN_ISSUES.md)

## 📄 Lizenz
MIT
