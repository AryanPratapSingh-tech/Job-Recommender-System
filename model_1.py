import streamlit as st
from src.utility_meth import extract_text_from_pdf, ask_GPT
from src.job_api import fetch_LinkedIn_Jobs, fetch_Naukari_Jobs

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="🤖",
    layout="wide"
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
}
.sub-text {
    font-size: 18px;
    color: #b0b0b0;
}
.card {
    background-color: #0e1117;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #262730;
    font-size: 16px;
}
.section-title {
    font-size: 24px;
    font-weight: 600;
}
.job-card {
    background-color: #0e1117;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #262730;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🤖 AI Job Recommender</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-text'>Upload your resume and receive AI-powered job insights, skill gap analysis, and career roadmap.</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- FILE UPLOAD ----------
upload_file = st.file_uploader(
    "📄 Upload your resume (PDF only)",
    type=["pdf"]
)

# ---------- PROCESSING ----------
if upload_file:
    with st.spinner("🔍 Extracting resume content..."):
        resume_text = extract_text_from_pdf(pdf_path=upload_file)

    with st.spinner("🧠 Generating resume summary..."):
        summary = ask_GPT(f"Summarize this resume highlighting skills, education and experience:\n\n{resume_text}", max_tokens=400)

    with st.spinner("🛠️ Identifying skill gaps..."):
        skill_gaps = ask_GPT(
            f"Analyze this resume and highlight missing skills, certifications and experience:\n\n{resume_text}",max_tokens=400
        )

    with st.spinner("🚀 Creating career roadmap..."):
        roadmap = ask_GPT(f"Suggest a future roadmap including skills, certifications and industry exposure:\n\n{resume_text}",max_tokens=400)

    st.success("✅ Resume analysis completed")

    # ---------- RESULTS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>📑 Resume Summary</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>{summary}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-title'>🛠️ Skill Gaps & Missing Areas</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'>{skill_gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<div class='section-title'>🚀 Career Roadmap</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>{roadmap}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- JOB RECOMMENDATION ----------
    if st.button("🔎 Get AI-Powered Job Recommendations"):
        with st.spinner("📌 Generating job keywords..."):
            keywords = ask_GPT(
                f"Suggest job titles and keywords (comma-separated only) based on this summary:\n\n{summary}",max_tokens=400
            )
            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"🎯 Job Search Keywords: {search_keywords_clean}")

        with st.spinner("🌐 Fetching jobs from LinkedIn & Naukri..."):
            linkedin_jobs = fetch_LinkedIn_Jobs(search_keywords_clean, rows=60)
            naukari_jobs = fetch_Naukari_Jobs(search_keywords_clean, rows=60)

        # ---------- JOB RESULTS ----------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-title'>💼 LinkedIn Jobs</div>", unsafe_allow_html=True)
            if linkedin_jobs:
                for job in linkedin_jobs:
                    st.markdown(f"""
                    <div class='job-card'>
                        <strong>{job.get('title')}</strong><br>
                        {job.get('companyName')}<br>
                        📍 {job.get('location')}<br>
                        🔗 <a href="{job.get('link')}" target="_blank">View Job</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No LinkedIn jobs found.")

        with col2:
            st.markdown("<div class='section-title'>🇮🇳 Naukri Jobs</div>", unsafe_allow_html=True)
            if naukari_jobs:
                for job in naukari_jobs:
                    st.markdown(f"""
                    <div class='job-card'>
                        <strong>{job.get('title')}</strong><br>
                        {job.get('companyName')}<br>
                        📍 {job.get('location')}<br>
                        🔗 <a href="{job.get('url')}" target="_blank">View Job</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No Naukri jobs found.")
