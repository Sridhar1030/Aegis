import logging

from models.state import AegisState

logger = logging.getLogger("aegis.guard")

LATENCY_THRESHOLD = 0.5
RISK_THRESHOLD = 0.6


def guard_agent(state: AegisState) -> AegisState:
    latency = state.get("replay_latency_delta") or 0
    risk = state.get("risk_score") or 0

    anomaly = latency > LATENCY_THRESHOLD or risk > RISK_THRESHOLD

    state["anomaly_detected"] = anomaly

    if anomaly:
        reasons = []
        if latency > LATENCY_THRESHOLD:
            reasons.append(f"latency {latency:.3f}s > {LATENCY_THRESHOLD}s threshold")
        if risk > RISK_THRESHOLD:
            reasons.append(f"risk score {risk} > {RISK_THRESHOLD} threshold")

        logger.warning(f"ANOMALY DETECTED: {', '.join(reasons)}")
        logger.warning("ROLLBACK TRIGGERED — deployment blocked")
    else:
        logger.info(f"All clear — latency={latency:.3f}s, risk={risk}")

    return state
