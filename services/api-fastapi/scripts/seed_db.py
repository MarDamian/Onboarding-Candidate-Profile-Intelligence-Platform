import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.db.models.candidate import Candidate

def seed():
    """
    Inserta datos de prueba en la base de datos.
    """
    db = SessionLocal()
    candidates = [
        Candidate(
            name="Oscar Osorio", 
            email="oscar@wtredata.com", 
            phone="123456", 
            location="Medellín", 
            headline="Fullstack Dev",
            summary="Experto en Python y FastAPI",
            role="Senior Developer",               
            experience="5 años en wTreData",       
            skills="Python, React, IA",            
            education="Ingeniería de Sistemas"     
        ),
        Candidate(
            name="Damian Martinez", 
            email="damian@wtredata.com", 
            phone="654321", 
            location="Bogotá", 
            headline="Backend Dev",
            summary="Especialista en arquitecturas",
            role="Backend Lead",                   
            experience="4 años en sistemas",       
            skills="Rust, PostgreSQL, Docker",     
            education="Ciencias de la Computación" 
        )
    ]
    try:
        for c in candidates:
            exists = db.query(Candidate).filter(Candidate.email == c.email).first()
            if not exists:
                db.add(c)
        db.commit()
        print("Seeds insertados con éxito")
    except Exception as e:
        print(f"Error al insertar seeds: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()