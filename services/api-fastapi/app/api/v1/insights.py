from fastapi import APIRouter, HTTPException
from app.llm.agent import Agent
from app.db.database import SessionLocal
from app.db.models.candidate import Candidate
from app.schemas.insight import InsightSchema
from app.llm.compression import ContextCompressor

router = APIRouter(prefix="/insights",tags=["LLM Insights"])

@router.get("/{candidate_id}",
    response_model=InsightSchema,
    responses={
        200: {"description": "Candidate insights generated successfully"},
        404: {"description": "Candidate not found"},
        422: {"description": "Invalid query parameters"}
    },
    summary="Genera insights para un candidato",
    description="Genera insights para un candidato filtrando por el id del candidato"
)
async def generate_candidate_insights(candidate_id: int):
    """
    Endpoint para visualizar insights en la UI de React.
    """
    db = SessionLocal()
    try:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    finally:
        db.close()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate_dict = {
        "summary": candidate.summary,
        "skills": candidate.skills.split(",") if candidate.skills else [],
        "experience": []
    } 
    
    compressed_context = ContextCompressor.to_prompt_context(candidate_dict)
    
    agent = Agent()
    query = f"Analiza este perfil comprimido y genera insights: {compressed_context}"
    
    insights = await agent.generate_insight(query=query)
    
    return {
        "candidate_id": candidate_id,
        "insights": insights
    }