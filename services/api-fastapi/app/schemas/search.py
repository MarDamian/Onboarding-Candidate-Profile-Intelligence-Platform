from pydantic import BaseModel, Field
from typing import Optional

class SearchRequest(BaseModel):
    """Schema para búsqueda semántica."""
    query: str = Field(..., min_length=3, description="Texto de búsqueda")
    limit: int = Field(default=10, ge=1, le=50, description="Número máximo de resultados")
    score_threshold: float = Field(default=0.2, ge=0.0, le=1.0, description="Umbral mínimo de similitud")
    skills_filter: Optional[list[str]] = Field(default=None, description="Filtrar por skills específicas")
    name_filter: Optional[str] = Field(default=None, description="Filtrar por nombre del candidato")
