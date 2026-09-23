import json
from pathlib import Path
from .memory import MemoryStore
from .turn_lock import TurnManager
from .events import EventBus
from backend.agents.base import Agent
from backend.providers.local_hf import LocalHFProvider

class Orchestrator:
    def __init__(self, agents, bus: EventBus, turns: TurnManager):
        self.agents={a.id:a for a in agents if a.enabled}
        self.bus=bus
        self.turns=turns
        self.memory=MemoryStore()
        self.ai=LocalHFProvider()

    async def choose(self,text:str)->Agent:
        options="\n".join(f"- {a.id}: {a.role} | {a.personality}" for a in self.agents.values())
        messages=[
            {"role":"system","content":"Du bist der Router eines Multi-Agent-Teams. Gib nur eine vorhandene Agent-ID zurück."},
            {"role":"user","content":f"Agenten:\n{options}\n\nAufgabe:\n{text}"}
        ]
        try:
            selected=(await self.ai.chat(messages)).strip().lower()
            return self.agents.get(selected) or max(self.agents.values(),key=lambda a:a.priority)
        except Exception:
            return max(self.agents.values(),key=lambda a:a.priority)

    async def _run(self,agent:Agent,prompt:str):
        return await self.ai.chat([
            {"role":"system","content":agent.prompt()},
            {"role":"user","content":prompt},
        ])

    async def _delegate(self,source:Agent,target_id:str,task:str)->str:
        target=self.agents.get(target_id)
        if not target or target.id==source.id:
            return "Kein passender Teamagent gefunden."
        await self.bus.publish({"type":"agent_message","from":source.id,"to":target.id,"content":task})
        result=await self._run(target,f"Interne Teamaufgabe von {source.name}:\n{task}\n\nGib nur deine fachliche Erkenntnis für das Team zurück.")
        await self.bus.publish({"type":"agent_result","from":target.id,"to":source.id,"content":result})
        return result

    async def ask(self,text:str)->dict:
        self.memory.add("user",text)
        agent=await self.choose(text)
        await self.bus.publish({"type":"agent_selected","agent":agent.id,"name":agent.name})
        history="\n".join(f"{x['role']}: {x['content']}" for x in self.memory.recent())
        draft=await self._run(agent,f"Gespräch:\n{history}\n\nNeue Aufgabe:\n{text}\n\nWenn du einen anderen Spezialisten brauchst, schreibe einmal [ASK_AGENT:agent_id] interne Aufgabe. Sonst antworte direkt.")
        final=draft
        if "[ASK_AGENT:" in draft:
            start=draft.find("[ASK_AGENT:")
            end=draft.find("]",start)
            if end!=-1:
                target=draft[start+11:end].strip()
                task=draft[end+1:].strip()
                internal=await self._delegate(agent,target,task)
                final=await self._run(agent,f"Entwurf:\n{draft}\n\nInterne Antwort:\n{internal}\n\nFormuliere die finale Antwort für den Nutzer. Keine internen Markierungen.")
        agent.remember("user",text)
        agent.remember("assistant",final)
        self.memory.add("assistant",final,agent.id)
        return {"agent":agent.id,"name":agent.name,"voice":agent.voice,"text":final}

def load_agents():
    path=Path(__file__).resolve().parents[2]/"config"/"agents.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    return [Agent(**item) for item in data["agents"]]
