"""
Servicio de encolamiento automático de jobs de indexación.

Encola jobs al Redis queue que escucha el worker Rust, para que cada
operación CRUD sobre candidatos dispare la actualización automática
del índice vectorial en Qdrant.
"""
import json
import logging
from datetime import datetime, timezone

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: redis.Redis | None = None


def _get_redis() -> redis.Redis:
    """Obtiene o crea la conexión Redis (singleton lazy)."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
    return _redis_client


def enqueue_single_index(candidate_id: int, requested_by: str = "fastapi") -> None:
    """Encola un job para indexar un candidato individual tras create/update."""
    payload = {
        "job_type": "single_index",
        "candidate_id": candidate_id,
        "requested_by": requested_by,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        _get_redis().rpush(settings.REDIS_QUEUE, json.dumps(payload))
        logger.info(
            "Job single_index encolado",
            extra={"candidate_id": candidate_id},
        )
    except Exception as e:
        # No bloquear la operación CRUD si Redis falla
        logger.error(
            "Error encolando single_index: %s", str(e),
            extra={"candidate_id": candidate_id},
        )


def enqueue_delete_point(candidate_id: int, requested_by: str = "fastapi") -> None:
    """Encola un job para eliminar el vector de un candidato borrado."""
    payload = {
        "job_type": "delete_point",
        "candidate_id": candidate_id,
        "requested_by": requested_by,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        _get_redis().rpush(settings.REDIS_QUEUE, json.dumps(payload))
        logger.info(
            "Job delete_point encolado",
            extra={"candidate_id": candidate_id},
        )
    except Exception as e:
        logger.error(
            "Error encolando delete_point: %s", str(e),
            extra={"candidate_id": candidate_id},
        )
