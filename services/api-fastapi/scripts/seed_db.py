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
        ),
        Candidate(
            name="María García",
            email="maria@wtredata.com",
            phone="111222",
            location="Madrid",
            headline="Senior Python Developer",
            summary="Desarrolladora Python con 8 años de experiencia en machine learning y data science",
            role="Machine Learning Engineer",
            experience="8 años en ML y AI",
            skills="Python, TensorFlow, Scikit-learn, Pandas",
            education="Maestría en Inteligencia Artificial"
        ),
        Candidate(
            name="Juan López",
            email="juan@wtredata.com",
            phone="333444",
            location="Buenos Aires",
            headline="Frontend Engineer",
            summary="Ingeniero frontend especializado en React y TypeScript",
            role="Senior Frontend Developer",
            experience="6 años en desarrollo web",
            skills="React, TypeScript, Next.js, TailwindCSS",
            education="Ingeniería Informática"
        ),
        Candidate(
            name="Ana Torres",
            email="ana@wtredata.com",
            phone="555666",
            location="Lima",
            headline="DevOps Engineer",
            summary="Experta en infraestructura cloud y automatización con AWS y Kubernetes",
            role="DevOps Lead",
            experience="7 años en DevOps",
            skills="AWS, Kubernetes, Docker, Terraform, CI/CD",
            education="Ingeniería de Sistemas"
        ),
        Candidate(
            name="Carlos Ruiz",
            email="carlos@wtredata.com",
            phone="777888",
            location="Ciudad de México",
            headline="Data Engineer",
            summary="Ingeniero de datos especializado en pipelines ETL y data warehousing",
            role="Senior Data Engineer",
            experience="5 años en ingeniería de datos",
            skills="Python, Spark, Airflow, SQL, Redshift",
            education="Ingeniería en Computación"
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