import asyncio
class EventBus:
 def __init__(self): self._subs=[]
 def subscribe(self,fn): self._subs.append(fn)
 async def publish(self,event): await asyncio.gather(*(fn(event) for fn in list(self._subs)),return_exceptions=True)
