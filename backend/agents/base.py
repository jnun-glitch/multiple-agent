from dataclasses import dataclass,field
@dataclass
class Agent:
 id:str; name:str; role:str; personality:str; voice:str; priority:int=50; enabled:bool=True
 memory:list[dict[str,str]]=field(default_factory=list)
 def prompt(self):
  return f"""Du bist {self.name}. Rolle: {self.role}. Persönlichkeit: {self.personality}.
Du bist Teil eines Multi-Agent-Teams. Bleibe deiner Rolle treu und unterbrich keinen anderen Sprecher."""
 def remember(self,role,content):
  self.memory.append({"role":role,"content":content}); self.memory=self.memory[-20:]
