import httpx
import time
import logging

from models.state import AegisState

logger = logging.getLogger("aegis.replay")

SAMPLE_REQUESTS = [
    {"path": "/"},
    {"path": "/"},
    {"path": "/slow"},
    {"path": "/"},
    {"path": "/slow"},
]

DEMO_SERVICE_URL = "http://localhost:8001"


def replay_agent(state: AegisState) -> AegisState:
    urls = [DEMO_SERVICE_URL + r["path"] for r in SAMPLE_REQUESTS]

    total_latency = 0.0
    errors = 0

    with httpx.Client(timeout=10.0) as client:
        for url in urls:
            start = time.time()
            try:
                resp = client.get(url)
                resp.raise_for_status()
            except Exception as e:
                errors += 1
                logger.warning(f"Request to {url} failed: {e}")
            total_latency += time.time() - start

    avg_latency = total_latency / len(urls)
    logger.info(f"Replay complete: avg_latency={avg_latency:.3f}s, errors={errors}/{len(urls)}")

    state["replay_latency_delta"] = round(avg_latency, 3)
    return state
