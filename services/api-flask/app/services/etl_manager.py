from pipelines.etl.main import run_pipeline
from app.core.config import settings

import json
import redis


class ETLManager:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)

    def trigger_sync(self):
        """_summary_

        Returns:
            _type_: _description_
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
