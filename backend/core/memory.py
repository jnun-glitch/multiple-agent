class MemoryStore:
 def __init__(self,max_items=80): self.items=[]; self.max_items=max_items
 def add(self,role,content,agent=None):
  self.items.append({"role":role,"content":content,"agent":agent}); self.items=self.items[-self.max_items:]
 def recent(self,n=12): return self.items[-n:]
