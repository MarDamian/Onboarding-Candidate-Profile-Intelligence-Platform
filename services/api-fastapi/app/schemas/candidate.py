from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: Optional[str] = None

    education: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    role: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(CandidateBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None

    education: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    role: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None

class CandidateRead(CandidateBase):
    id: int
    
    is_active: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
