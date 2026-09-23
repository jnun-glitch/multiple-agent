import asyncio,pytest
from backend.core.turn_lock import TurnManager
@pytest.mark.asyncio
async def test_exclusive_turn():
 m=TurnManager(); active=0; maximum=0
 async def w(x):
  nonlocal active,maximum
  async with m.speaking_turn(x):
   active+=1; maximum=max(maximum,active); await asyncio.sleep(.01); active-=1
 await asyncio.gather(w("a"),w("b"),w("c"))
 assert maximum==1
 assert not m.locked()
