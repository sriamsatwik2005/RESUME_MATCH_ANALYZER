import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ------------------------------
# Custom Styling
# ------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }
    .block-container {
        padding-top: 2rem;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Header
# ------------------------------
st.title("📄 Resume Analyzer & Job Matcher")
st.caption("AI-powered resume analysis using RAG")

# ------------------------------
# Upload Resume
# ------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ Upload Resume (PDF)")
resume_file = st.file_uploader("Choose a resume", type=["pdf"])
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Job Description
# ------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ Paste Job Description")
job_description = st.text_area(
    "Job description",
    height=180,
    placeholder="Paste the job description here..."
)
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Analyze Button
# ------------------------------
analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True)

# ------------------------------
# Logic
# ------------------------------
if analyze_btn:
    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):

            # 1. Upload job
            requests.post(
                f"{BACKEND_URL}/job/upload",
                json={
                    "job_id": "streamlit_job",
                    "job_description": job_description
                }
            )

            # 2. Upload resume
            res = requests.post(
                f"{BACKEND_URL}/upload-resume",
                files={"file": resume_file}
            )

            if res.status_code != 200:
                st.error("Resume upload failed")
                st.stop()

            resume_text = res.json().get("resume_text", "")

            # 3. Analyze
            analysis_res = requests.post(
                f"{BACKEND_URL}/analysis/resume-vs-job",
                json={"resume_text": resume_text}
            )

            if analysis_res.status_code != 200:
                st.error("Analysis failed")
                st.stop()

            data = analysis_res.json()

        # ------------------------------
        # Results
        # ------------------------------
        st.success("Analysis Complete 🎉")

        col1, col2 = st.columns(2)
        col1.metric("Skill Match %", f"{data['skill_match_percentage']}%")
        col2.metric("Role Fit Score", f"{data['role_fit_score']}%")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("✅ Matched Skills")
        st.write(", ".join(data["matched_skills"]) or "None")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("❌ Missing Skills")
        st.write(", ".join(data["missing_skills"]) or "None")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 Improvement Suggestions")
        st.write(data["improvement_suggestions"])
        st.markdown("</div>", unsafe_allow_html=True)
