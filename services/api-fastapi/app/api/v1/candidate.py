from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.candidate import Candidate
from app.db.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/candidate", tags=["Candidate"])

@router.get(
    "/", 
    response_model=list[CandidateRead], 
    status_code=200,
    responses={
        200: {"description": "List of candidates"},
        422: {"description": "Invalid query parameters"}
    },
    summary="Lista de candidatos",
    description="Lista de todos los candidatos"
)
def list_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates

@router.get(
    "/{candidate_id}", 
    response_model=CandidateRead, 
    status_code=200,
    responses={
        200: {"description": "Candidate found"},
        404: {"description": "Candidate not found"},
        422: {"description": "Invalid query parameters"}
    },
    summary="Candidato por ID",
    description="Obtiene un candidato filtrando por el id del candidato"
)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.post(
    "/", 
    response_model=CandidateCreate, 
    status_code=201, 
    responses={
        201: {"description": "Candidate created successfully"},
        400: {"description": "Invalid input"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"},
    },
    summary="Crear un nuevo candidato",
    description="Crea un nuevo candidato con sus respectivos datos"
)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    try:
        new_candidate = Candidate(**candidate.model_dump())
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)
        
        logger.info(
            f"Candidato creado exitosamente",
            extra={"candidate_id": new_candidate.id, "email": new_candidate.email}
        )
        
        return new_candidate
    
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower()
        
        if "email" in error_msg:
            logger.warning(
                f"Intento de crear candidato con email duplicado",
                extra={"email": candidate.email}
            )
            raise HTTPException(
                status_code=409,
                detail="El email ya está registrado en el sistema"
            )
        elif "phone" in error_msg:
            logger.warning(
                f"Intento de crear candidato con teléfono duplicado",
                extra={"phone": candidate.phone}
            )
            raise HTTPException(
                status_code=409,
                detail="El teléfono ya está registrado en el sistema"
            )
        else:
            logger.error(f"Error de integridad al crear candidato: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Error de validación en la base de datos"
            )
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear candidato: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@router.put(
    "/{candidate_id}", 
    response_model=CandidateUpdate,
    responses={
        200: {"description": "Candidate updated successfully"},
        404: {"description": "Candidate not found"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"}
    },
    summary="Actualizar un candidato",
    description="Actualiza un candidato filtrando por el id del candidato"
)
def update_candidate(candidate_id: int, candidate: CandidateUpdate, db: Session = Depends(get_db)):
    existing_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not existing_candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    try:
        # Actualizar solo los campos proporcionados
        if candidate.name is not None:
            existing_candidate.name = candidate.name

        if candidate.email is not None:
            existing_candidate.email = candidate.email

        if candidate.phone is not None:
            existing_candidate.phone = candidate.phone

        if candidate.location is not None:
            existing_candidate.location = candidate.location

        if candidate.education is not None:
            existing_candidate.education = candidate.education

        if candidate.headline is not None:
            existing_candidate.headline = candidate.headline

        if candidate.summary is not None:
            existing_candidate.summary = candidate.summary

        if candidate.role is not None:
            existing_candidate.role = candidate.role

        if candidate.experience is not None:
            existing_candidate.experience = candidate.experience

        if candidate.skills is not None:
            existing_candidate.skills = candidate.skills

        db.commit()
        db.refresh(existing_candidate)
        
        logger.info(
            f"Candidato actualizado exitosamente",
            extra={"candidate_id": candidate_id}
        )

        return existing_candidate
    
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower()
        
        if "email" in error_msg:
            logger.warning(
                f"Intento de actualizar candidato con email duplicado",
                extra={"candidate_id": candidate_id, "email": candidate.email}
            )
            raise HTTPException(
                status_code=409,
                detail="El email ya está registrado en el sistema"
            )
        elif "phone" in error_msg:
            logger.warning(
                f"Intento de actualizar candidato con teléfono duplicado",
                extra={"candidate_id": candidate_id, "phone": candidate.phone}
            )
            raise HTTPException(
                status_code=409,
                detail="El teléfono ya está registrado en el sistema"
            )
        else:
            logger.error(f"Error de integridad al actualizar candidato: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Error de validación en la base de datos"
            )
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar candidato: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@router.delete(
    "/{candidate_id}", 
    response_model=CandidateRead, 
    responses={
        200: {"description": "Candidate deleted successfully"},
        404: {"description": "Candidate not found"}
    },
    summary="Eliminar un candidato",
    description="Elimina un candidato filtrando por el id del candidato"
)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    db.delete(candidate)
    db.commit()
    
    logger.info(
        f"Candidato eliminado exitosamente",
        extra={"candidate_id": candidate_id}
    )
    
    return candidate