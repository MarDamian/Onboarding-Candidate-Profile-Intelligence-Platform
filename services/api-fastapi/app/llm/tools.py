from langchain.tools import tool
from app.db.database import SessionLocal
from app.db.models.candidate import Candidate
import os, httpx
import pydantic
from langchain_core.prompts import ChatPromptTemplate
from app.llm.prompt_loader import PromptLoader
from app.llm.compression import ContextCompressor
from langchain_cohere import ChatCohere

SEARCH_API_URL = os.getenv("SEARCH_API_URL", "http://127.0.0.1:8000/v1")

class ScoreResult(pydantic.BaseModel):
    score: float = pydantic.Field(description="Puntaje de 0.0 a 1.0")
    justification: str = pydantic.Field(description="Resumen de por qué se asignó ese puntaje")

@tool
def get_candidate_profile(candidate_id: int) -> dict:
    """Ontiene el perfil detallado de un candidato desde la base de datos SQL.

    Args:
        candidate_id (int): El identificador del candidato

    Returns:
        dict: La información detallada del candidato
    """
    db = SessionLocal()
    try:
        c = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not c: return "Candidato no encontrado."
        return f"Nombre: {c.name} | Headline: {c.headline} | Skills: {c.skills} | Experiencia: {c.experience} | Resumen: {c.summary}"
    finally:
        db.close()

@tool
def search_similar_profiles(candidate_id: int, limit: int = 3) -> str:
    """
    Busca candidatos similares a un candidato específico utilizando su ID.
    Esta herramienta es útil para comparar al candidato actual con otros perfiles 
    similares en la base de datos vectorial.

    Args:
        candidate_id (int): El ID del candidato de referencia.
        limit (int): Cantidad de perfiles similares a retornar.
    """
    url = f"{SEARCH_API_URL}/semantic_search/similar/{candidate_id}"
    params = {"limit": limit}

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            
            if response.status_code == 404:
                return f"Error: El candidato con ID {candidate_id} no está indexado en el motor vectorial."
            
            response.raise_for_status()
            results = response.json()
            
            return str(results.get("results", []))

    except httpx.RequestError as exc:
        return f"Error de conexión al intentar buscar similares: {exc}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

@tool
def calculate_score(candidate_data: str, job_description: str) -> str:
    """
    Calcula un puntaje de compatibilidad técnica y cultural entre un candidato 
    y una vacante específica. Utiliza razonamiento de IA para evaluar skills.

    Args:
        candidate_data (str): Información completa o comprimida del candidato.
        job_description (str): Requerimientos del puesto o descripción de la vacante.
    """
    
    compressed_candidate = ContextCompressor.compress(candidate_data)


    system_prompt = PromptLoader.get_prompt("skill_extraction", "v1")
    
    evaluator_llm = ChatCohere(model="command-a-03-2025", temperature=0)
    
    structured_llm = evaluator_llm.with_structured_output(ScoreResult)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Candidato: {candidate}\n\nVacante: {job}")
    ])

    chain = prompt | structured_llm

    try:
        result = chain.invoke({
            "candidate": compressed_candidate,
            "job": job_description
        })

        return f"Puntaje: {result.score}/1.0. Justificación: {result.justification}"

    except Exception as e:
        return f"Error calculando el score: {str(e)}. Fallback: Score estimado 0.5 (Revisión manual requerida)."