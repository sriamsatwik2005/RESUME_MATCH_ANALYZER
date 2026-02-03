from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.analyzer import analyze
from app.services.vectorstore import job_vector_store
from app.services.embeddings import embed_texts

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

class AnalysisRequest(BaseModel):
    resume_text: str
    top_k: int = 5

class AnalysisResponse(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    skill_match_percentage: int
    role_fit_score: int
    improvement_suggestions: str

@router.post("/resume-vs-job", response_model=AnalysisResponse)
def analyze_resume_against_job(request: AnalysisRequest):

    if not job_vector_store.texts:
        raise ValueError("No job description uploaded")

    query_embedding = embed_texts([request.resume_text])[0]

    job_chunks = job_vector_store.search(
        query_embedding=query_embedding,
        k=request.top_k
    )

    combined_job_text = "\n".join(job_chunks)

    return analyze(
        resume_text=request.resume_text,
        job_text=combined_job_text
    )
