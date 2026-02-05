from pydantic import BaseModel, Field
from typing import List

class InsightSchema(BaseModel):
    summary: str = Field(description="Resumen ejecutivo del candidato")
    score: int = Field(description="Puntaje de 0 a 100")
    strengths: List[str] = Field(description="Lista de fortalezas")
    weaknesses: List[str] = Field(description="Lista de áreas de mejora")
    suggested_role: str = Field(description="Rol sugerido para el candidato")