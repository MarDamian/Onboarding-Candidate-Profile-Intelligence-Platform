from fastapi import FastAPI
from app.api.v1 import candidate, search, insights
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Candidate Profile Intelligence Platform API",
    description="Api para gestionar candidatos",
    version="1.0.0"
)

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