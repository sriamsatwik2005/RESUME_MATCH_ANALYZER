import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Resume Analyzer & Job Matching System")
st.caption("Clean UI over FastAPI + RAG backend")

st.divider()

# -----------------------------
# Resume Upload
# -----------------------------
st.subheader("1️⃣ Upload Resume (PDF)")
resume_file = st.file_uploader("Choose your resume", type=["pdf"])

# -----------------------------
# Job Description
# -----------------------------
st.subheader("2️⃣ Paste Job Description")
job_description = st.text_area(
    "Job Description",
    height=180,
    placeholder="Paste the job description here..."
)

st.divider()

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🔍 Analyze Resume", use_container_width=True):

    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and paste a job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):

        # Upload job description
        requests.post(
            f"{BACKEND_URL}/job/upload",
            json={
                "job_id": "streamlit_job",
                "job_description": job_description
            }
        )

        # Upload resume
        res = requests.post(
            f"{BACKEND_URL}/upload-resume",
            files={"file": resume_file}
        )

        if res.status_code != 200:
            st.error("Resume upload failed")
            st.stop()

        resume_text = res.json().get("resume_text")
        if not resume_text:
            st.error("Resume text extraction failed (null response)")
            st.stop()

        # Analyze
        analysis_res = requests.post(
            f"{BACKEND_URL}/analysis/resume-vs-job",
            json={"resume_text": resume_text}
        )

        if analysis_res.status_code != 200:
            st.error("Analysis failed")
            st.stop()

        data = analysis_res.json()

    # -----------------------------
    # Results
    # -----------------------------
    st.success("Analysis Complete 🎉")

    col1, col2 = st.columns(2)
    col1.metric("Skill Match %", f"{data['skill_match_percentage']}%")
    col2.metric("Role Fit Score", f"{data['role_fit_score']}%")

    st.subheader("✅ Matched Skills")
    st.write(", ".join(data["matched_skills"]) or "None")

    st.subheader("❌ Missing Skills")
    st.write(", ".join(data["missing_skills"]) or "None")

    st.subheader("💡 Improvement Suggestions")
    st.write(data["improvement_suggestions"])
