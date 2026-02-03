from fastapi import FastAPI
from app.api import resume, job, analysis

app = FastAPI()

app.include_router(resume.router)
app.include_router(job.router)
app.include_router(analysis.router)
