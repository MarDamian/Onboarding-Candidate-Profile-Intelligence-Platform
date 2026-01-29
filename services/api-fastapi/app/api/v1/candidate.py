from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.candidate import Candidate
from app.db.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate

router = APIRouter(prefix="/candidate", tags=["Candidate"])

@router.get(
    "/", 
    response_model=list[CandidateRead], 
    status_code=200,
    responses={
        200: {"description": "List of candidates"},
        422: {"description": "Invalid query parameters"}
    }
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
    }
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
    }
)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    new_candidate = Candidate(**candidate.dict())
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

@router.put(
    "/{candidate_id}", 
    response_model=CandidateUpdate,
    responses={
        200: {"description": "Candidate updated successfully"},
        404: {"description": "Candidate not found"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"}
    }
)
def update_candidate(candidate_id: int, candidate: CandidateUpdate, db: Session = Depends(get_db)):
    update_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not update_candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    if candidate.name is not None:
        update_candidate.name = candidate.name

    if candidate.email is not None:
        update_candidate.email = candidate.email

    if candidate.phone is not None:
        update_candidate.phone = candidate.phone

    if candidate.location is not None:
        update_candidate.location = candidate.location

    if candidate.education is not None:
        update_candidate.education = candidate.education

    if candidate.headline is not None:
        update_candidate.headline = candidate.headline

    if candidate.summary is not None:
        update_candidate.summary = candidate.summary

    if candidate.role is not None:
        update_candidate.role = candidate.role

    if candidate.experience is not None:
        update_candidate.experience = candidate.experience

    if candidate.skills is not None:
        update_candidate.skills = candidate.skills

    db.commit()
    db.refresh(update_candidate)

    return update_candidate

@router.delete(
    "/{candidate_id}", 
    response_model=CandidateRead, 
    responses={
        204: {"description": "Candidate deleted successfully"},
        404: {"description": "Candidate not found"}
    }
)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate:
        db.delete(candidate)
        db.commit()
    return candidate