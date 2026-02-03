from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.chunker import chunk_text
from app.services.embeddings import embed_texts
from app.services.vectorstore import job_vector_store

router = APIRouter(
    prefix="/job",
    tags=["Job Description"]
)

# -----------------------------
# Pydantic Models
# -----------------------------

class JobUploadRequest(BaseModel):
    job_id: str
    job_description: str


class JobSearchResponse(BaseModel):
    matched_requirements: List[str]


# -----------------------------
# Upload Job Description
# -----------------------------

@router.post("/upload")
def upload_job_description(job: JobUploadRequest):
    """
    Ingest a job description:
    1. Chunk text
    2. Generate embeddings
    3. Store in FAISS vector DB
    """

    # Step 1: Chunk job description
    chunks = chunk_text(job.job_description)

    # Step 2: Generate embeddings
    embeddings = embed_texts(chunks)

    # Step 3: Store in vector DB
    job_vector_store.add(embeddings, chunks)

    return {
        "message": "Job description uploaded successfully",
        "job_id": job.job_id,
        "total_chunks": len(chunks)
    }


# -----------------------------
# Semantic Search Job Requirements
# -----------------------------

@router.get("/search", response_model=JobSearchResponse)
def search_job_requirements(query: str, top_k: int = 5):
    """
    Semantic search over stored job descriptions
    """

    # Generate embedding for query
    query_embedding = embed_texts([query])[0]

    # Search vector DB
    matched_chunks = job_vector_store.search(
        query_embedding=query_embedding,
        k=top_k
    )

    return {
        "matched_requirements": matched_chunks
    }
