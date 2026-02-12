from fastapi import FastAPI
from app.api.v1 import candidate, search, insights
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging
from app.core.exceptions import (
    integrity_error_handler,
    duplicate_resource_error_handler,
    resource_not_found_error_handler,
    DuplicateResourceError,
    ResourceNotFoundError
)
from sqlalchemy.exc import IntegrityError

# Initialize structured logging
setup_logging()

app = FastAPI(
    title="Candidate Profile Intelligence Platform API",
    description="Api para gestionar candidatos",
    version="1.0.0"
)

# Registrar manejadores de excepciones globales
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(DuplicateResourceError, duplicate_resource_error_handler)
app.add_exception_handler(ResourceNotFoundError, resource_not_found_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(candidate.router, prefix="/v1")
app.include_router(search.router, prefix="/v1")
app.include_router(insights.router, prefix="/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}