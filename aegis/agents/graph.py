from langgraph.graph import StateGraph
from models.state import AegisState
from agents.risk_agent import risk_agent


def replay_stub(state: AegisState):
    state["replay_latency_delta"] = 0.2
    return state


builder = StateGraph(AegisState)

builder.add_node("replay", replay_stub)
builder.add_node("risk", risk_agent)

builder.set_entry_point("replay")
builder.add_edge("replay", "risk")

graph = builder.compile()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../.env")

    result = graph.invoke({"pr_id": "123"})
    print(result)
