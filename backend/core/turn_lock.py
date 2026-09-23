import asyncio
from contextlib import asynccontextmanager
class TurnManager:
 def __init__(self): self._lock=asyncio.Lock(); self.current_speaker=None
 @asynccontextmanager
 async def speaking_turn(self,agent_id):
  await self._lock.acquire(); self.current_speaker=agent_id
  try: yield
  finally: self.current_speaker=None; self._lock.release()
 def locked(self): return self._lock.locked()
