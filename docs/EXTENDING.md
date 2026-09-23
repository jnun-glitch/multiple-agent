# 🧩 Extending

<details><summary>Agent</summary>
Agenten über `config/agents.json` registrieren. Für Sonderlogik ein eigenes Modul unter `backend/agents/` ergänzen.
</details>

<details><summary>Skill</summary>
Tool implementieren → in ToolRegistry registrieren → Berechtigungen festlegen → Tests hinzufügen.
</details>

<details><summary>Provider</summary>
Voice, LLM und zukünftige Vision/Image-Dienste sollten hinter kleinen Service-Interfaces bleiben.
</details>