from sqlalchemy import create_engine, text

class Extractor:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        
    def get_stale_candidate(self):
        """Extrae candidatos que nunca se han indexado o que cambiaron después de indexarse.
        """
        query = text("""
            SELECT id, name, summary, skills, experience, updated_at
            FROM candidates
            WHERE last_indexed_at IS NULL OR updated_at > last_indexed_at             
        """)
        
        with self.engine.connect() as conn:
            return conn.execute(query).fetchall()
