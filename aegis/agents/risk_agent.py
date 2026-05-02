import json
import os
from groq import Groq
from models.risk import RiskOutput
from models.state import AegisState

SYSTEM_PROMPT = """You are a senior software risk analyst. Given metrics from a PR analysis pipeline, assess the deployment risk.

You MUST respond with valid JSON matching this schema:
{
  "score": <float 0-1>,
  "reasoning": "<brief explanation>"
}

Scoring guide:
- 0.0-0.3: Low risk — safe to deploy
- 0.3-0.6: Medium risk — review recommended
- 0.6-0.8: High risk — senior review required
- 0.8-1.0: Critical — block deployment"""


def risk_agent(state: AegisState) -> AegisState:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    user_prompt = f"""Analyze the following PR metrics and provide a risk assessment:

- PR ID: {state.get("pr_id")}
- SonarQube Score: {state.get("sonar_score", "not available")}
- Replay Latency Delta: {state.get("replay_latency_delta", "not available")}
- Chaos Resilience Score: {state.get("chaos_resilience_score", "not available")}

Return your assessment as JSON with "score" (0-1) and "reasoning" fields."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw = json.loads(response.choices[0].message.content)
    output = RiskOutput(**raw)

    state["risk_score"] = output.score
    state["risk_reasoning"] = output.reasoning
    return state
