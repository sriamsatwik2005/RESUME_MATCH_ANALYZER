def analyze(resume_text: str, job_text: str):

    resume_lower = resume_text.lower()
    job_lower = job_text.lower()

    job_keywords = list(set(job_lower.split()))
    matched = [k for k in job_keywords if k in resume_lower]
    missing = [k for k in job_keywords if k not in resume_lower]

    match_percent = int((len(matched) / max(len(job_keywords), 1)) * 100)

    return {
        "matched_skills": matched[:10],
        "missing_skills": missing[:10],
        "skill_match_percentage": match_percent,
        "role_fit_score": min(match_percent + 10, 100),
        "improvement_suggestions": "Improve missing skills and align resume keywords with job description."
    }
