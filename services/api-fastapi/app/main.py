from fastapi import FastAPI
from app.api.v1 import candidate
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Candidate Profile Intelligence Platform API",
    description="Api para gestionar candidatos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

app.include_router(candidate.router, prefix="/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}