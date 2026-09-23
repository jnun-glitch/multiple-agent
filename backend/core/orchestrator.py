import json
from pathlib import Path
from openai import AsyncOpenAI
from config.settings import CHAT_MODEL
from .memory import MemoryStore
from .turn_lock import TurnManager
from .events import EventBus
from backend.agents.base import Agent

class Orchestrator:
    def __init__(self, agents, bus: EventBus, turns: TurnManager):
        self.agents={a.id:a for a in agents if a.enabled}
        self.bus=bus
        self.turns=turns
        self.memory=MemoryStore()
        self.client=AsyncOpenAI()

    async def choose(self, text:str)->Agent:
        options="\n".join(f"- {a.id}: {a.role} | {a.personality}" for a in self.agents.values())
        try:
            r=await self.client.responses.create(
                model=CHAT_MODEL,
                instructions="Du bist der Router eines Multi-Agent-Teams. Gib nur eine vorhandene Agent-ID zurück.",
                input=f"Agenten:\n{options}\n\nAufgabe:\n{text}"
            )
            selected=r.output_text.strip().lower()
            return self.agents.get(selected) or max(self.agents.values(),key=lambda a:a.priority)
        except Exception:
            return max(self.agents.values(),key=lambda a:a.priority)

    async def _run(self, agent:Agent, prompt:str):
        r=await self.client.responses.create(
            model=CHAT_MODEL,
            instructions=agent.prompt(),
            input=prompt
        )
        return r.output_text.strip()

    async def _delegate(self, source:Agent, target_id:str, task:str)->str:
        target=self.agents.get(target_id)
        if not target or target.id==source.id:
            return "Kein passender Teamagent gefunden."
        await self.bus.publish({
            "type":"agent_message",
            "from":source.id,
            "to":target.id,
            "content":task
        })
        result=await self._run(
            target,
            f"Interne Teamaufgabe von {source.name}:\n{task}\n\nGib nur deine fachliche Erkenntnis für das Team zurück."
        )
        await self.bus.publish({
            "type":"agent_result",
            "from":target.id,
            "to":source.id,
            "content":result
        })
        return result

    async def ask(self, text:str)->dict:
        self.memory.add("user",text)
        agent=await self.choose(text)
        await self.bus.publish({"type":"agent_selected","agent":agent.id,"name":agent.name})

        history="\n".join(f"{x['role']}: {x['content']}" for x in self.memory.recent())
        prompt=f"""Gespräch:
{history}

Neue Nutzeraufgabe:
{text}

Du bist der ausgewählte Sprecher {agent.name}.
Falls du für die Aufgabe einen anderen Spezialisten brauchst, fordere ihn genau einmal an:
[ASK_AGENT:agent_id] konkrete interne Aufgabe

Wenn du keine Delegation brauchst, antworte direkt.
"""
        draft=await self._run(agent,prompt)

        if "[ASK_AGENT:" in draft:
            start=draft.find("[ASK_AGENT:")
            end=draft.find("]",start)
            if end!=-1:
                target_id=draft[start+11:end].strip()
                task=draft[end+1:].strip()
                internal=await self._delegate(agent,target_id,task)
                final=await self._run(
                    agent,
                    f"Ursprünglicher Entwurf:\n{draft}\n\nInterne Antwort von {target_id}:\n{internal}\n\nFormuliere jetzt ausschließlich die finale Antwort an den Nutzer. Keine internen Markierungen."
                )
            else:
                final=draft
        else:
            final=draft

        agent.remember("user",text)
        agent.remember("assistant",final)
        self.memory.add("assistant",final,agent.id)
        return {"agent":agent.id,"name":agent.name,"voice":agent.voice,"text":final}

def load_agents():
    path=Path(__file__).resolve().parents[2]/"config"/"agents.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    return [Agent(**item) for item in data["agents"]]
