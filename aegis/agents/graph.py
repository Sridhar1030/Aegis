from langgraph.graph import StateGraph
from models.state import AegisState


def replay_stub(state: AegisState):
    state["replay_latency_delta"] = 0.2
    return state


def risk_stub(state: AegisState):
    state["risk_score"] = 0.5
    state["risk_reasoning"] = "Mock reasoning"
    return state


builder = StateGraph(AegisState)

builder.add_node("replay", replay_stub)
builder.add_node("risk", risk_stub)

builder.set_entry_point("replay")
builder.add_edge("replay", "risk")

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"pr_id": "123"})
    print(result)
