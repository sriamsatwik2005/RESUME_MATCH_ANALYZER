from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.services.parser import extract_text_from_pdf

router = APIRouter(tags=["Resume"])

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    os.makedirs("data/resumes", exist_ok=True)

    file_path = f"data/resumes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    return {
        "message": "Resume uploaded successfully",
        "resume_text": resume_text
    }
