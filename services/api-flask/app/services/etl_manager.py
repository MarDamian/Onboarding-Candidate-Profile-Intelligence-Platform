from pipelines.etl.main import run_pipeline
from app.core.config import settings

import json
import redis
from datetime import datetime


class ETLManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.queue_name = "jobs:etl"

    def trigger_sync(self, requested_by: str = "api"):
        """
        Envía un job de ETL sync a la cola de Redis para procesamiento asíncrono.
        
        Args:
            requested_by: Usuario o sistema que solicita el job
            
        Returns:
            dict: Información del job encolado
        """
        job_payload = {
            "job_type": "etl_sync",
            "requested_by": requested_by,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Enviar job a la cola de Redis para el worker Rust
        self.redis_client.rpush(self.queue_name, json.dumps(job_payload))
        
        return {
            "status": "job_queued",
            "queue": self.queue_name,
            "job_payload": job_payload
        }
    
    def trigger_sync_direct(self):
        """
        Ejecuta el pipeline ETL de forma síncrona (método legacy).
        Útil para debugging o ejecuciones manuales.
        
        Returns:
            int: Número de registros procesados
        """
        return run_pipeline()

    def get_execution_history(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        last_job_key = "etl:last:job"
        data = self.redis_client.get(last_job_key)
        if not data:
            return {"status": "idle", "message": "No jobs found"}

        return json.loads(data)
    
    def get_executions(self, limit: int = 50):
        """Obtiene el historial de ejecuciones de ETL desde Redis."""
        executions = self.redis_client.lrange('etl_executions', -limit, -1)
        return [json.loads(exec) for exec in executions]
