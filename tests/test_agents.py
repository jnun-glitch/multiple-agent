from backend.core.orchestrator import load_agents
def test_agents(): assert len(load_agents())>=5
