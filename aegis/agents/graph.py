from langgraph.graph import StateGraph
from models.state import AegisState
from agents.replay_agent import replay_agent
from agents.memory_agent import memory_agent
from agents.risk_agent import risk_agent
from agents.guard_agent import guard_agent


builder = StateGraph(AegisState)

builder.add_node("replay", replay_agent)
builder.add_node("memory", memory_agent)
builder.add_node("risk", risk_agent)
builder.add_node("guard", guard_agent)

builder.set_entry_point("replay")
builder.add_edge("replay", "memory")
builder.add_edge("memory", "risk")
builder.add_edge("risk", "guard")

graph = builder.compile()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../.env")

    result = graph.invoke({"pr_id": "123"})
    print(result)
