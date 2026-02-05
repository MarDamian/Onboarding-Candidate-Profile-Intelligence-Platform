from datetime import datetime
from pipelines.etl.extract import Extractor
from pipelines.etl.transform import Transformer
from pipelines.etl.load import Loader
from dotenv import load_dotenv
import os, redis, json

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
QDRANT_HOST = os.getenv("QDRANT_HOST")
REDIS_URL = os.getenv("REDIS_URL")

r = redis.from_url(REDIS_URL)

def log_execution(status: str, message: str, processed: int, error: str = None):
    """Loggea una ejecución de ETL en Redis para seguimiento."""
    execution = {
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'message': message,
        'processed': processed,
        'error': error
    }
    r.rpush('etl_executions', json.dumps(execution))

def run_pipeline():
    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    status_key = f"etl:job:{job_id}"

    try:
        r.set(status_key, json.dumps({"status": "extracting", "start_time": job_id}))

        extractor = Extractor(DB_URL)
        transformer = Transformer()
        loader = Loader(QDRANT_HOST, DB_URL)

        loader.ensure_collection()

        raw_data = extractor.get_stale_candidate()
        if not raw_data:
            r.set(status_key, json.dumps({"status": "success", "message": "No new data"}))
            return 0

        r.set(status_key, json.dumps({"status": "transforming", "count": len(raw_data)}))
        processed_data = [transformer.prepare_vector(c) for c in raw_data]

        r.set(status_key, json.dumps({"status": "loading", "count": len(processed_data)}))
        loader.load_points(processed_data)

        candidate_ids = [p['id'] for p in processed_data]
        loader.mark_as_indexed(candidate_ids)
        
        processed = len(candidate_ids)

        final_status = {
            "status": "completed",
            "processed": processed,
            "finished_at": str(datetime.now())
        }
        r.set(status_key, json.dumps(final_status))
        r.set("etl:last_success_job", status_key)
        
        log_execution('success', 'ETL completed', processed)
        
        return {
            'status': 'success', 
            'message': 'ETL completed', 
            'processed': processed
        }

    except Exception as e:
        log_execution('error', 'ETL failed', 0, str(e))
        error_status = {"status": "failed", "error": str(e)}
        r.set(status_key, json.dumps(error_status))
        raise e
