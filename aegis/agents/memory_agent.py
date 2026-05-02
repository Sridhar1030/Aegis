import os
import logging
import psycopg2
from sentence_transformers import SentenceTransformer

from models.state import AegisState

logger = logging.getLogger("aegis.memory")

model = SentenceTransformer("all-MiniLM-L6-v2")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": os.getenv("POSTGRES_DB", "aegis"),
    "user": os.getenv("POSTGRES_USER", "aegis"),
    "password": os.getenv("POSTGRES_PASSWORD", "aegis"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def embed(text: str) -> list[float]:
    return model.encode(text).tolist()


def search_similar_failures(description: str, top_k: int = 3) -> list[str]:
    query_vec = embed(description)
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT description, embedding <=> %s::vector AS distance
                FROM failures
                ORDER BY distance
                LIMIT %s
                """,
                (str(query_vec), top_k),
            )
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def memory_agent(state: AegisState) -> AegisState:
    latency = state.get("replay_latency_delta", 0)
    description = f"Deployment showing average latency of {latency}s on replayed traffic"

    similar = search_similar_failures(description)
    logger.info(f"Found {len(similar)} similar past failures")

    state["similar_failures"] = similar
    return state
