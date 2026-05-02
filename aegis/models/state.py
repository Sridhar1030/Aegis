from typing import TypedDict, Optional

class AegisState(TypedDict):
    pr_id: str
    sonar_score: Optional[float]
    replay_latency_delta: Optional[float]
    chaos_resilience_score: Optional[float]
    risk_score: Optional[float]
    risk_reasoning: Optional[str]