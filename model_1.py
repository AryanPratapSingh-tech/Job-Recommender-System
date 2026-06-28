import streamlit as st
from src.utility_meth import extract_text_from_pdf
from src.job_api import fetch_LinkedIn_Jobs, fetch_Naukari_Jobs
from ollama_inst import Ollama_action
 
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="🤖",
    layout="wide"
)
 
# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
 
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
 
  .hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4f8ef7, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
  }
  .hero-sub {
    font-size: 1rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
  }
  .section-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px 24px;
    font-size: 15px;
    color: #e5e7eb;
    line-height: 1.7;
    margin-bottom: 1rem;
  }
  .section-label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 8px;
  }
  .job-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 4px solid #4f8ef7;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #e5e7eb;
  }
  .job-card a {
    color: #60a5fa;
    text-decoration: none;
    font-weight: 600;
  }
  .job-card a:hover { text-decoration: underline; }
  .badge {
    display: inline-block;
    background: #1e3a5f;
    color: #93c5fd;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 12px;
    margin-right: 6px;
  }
  .stButton > button {
    background: linear-gradient(90deg, #4f8ef7, #a78bfa);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .stButton > button:hover { opacity: 0.88; }
</style>
""", unsafe_allow_html=True)
 
# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("<div class='hero-title'>🤖 AI Job Recommender</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>Upload your résumé · Get AI-powered insights · Discover matching jobs — all free, all local.</div>",
    unsafe_allow_html=True
)
st.markdown("---")
 
# ── File upload ───────────────────────────────────────────────────────────────
upload_file = st.file_uploader("📄 Upload your résumé (PDF only)", type=["pdf"])
 
# ── Resume processing ─────────────────────────────────────────────────────────
if upload_file:
 
    with st.spinner("🔍 Extracting text from your résumé..."):
        resume_text = extract_text_from_pdf(pdf_path=upload_file)
 
    if not resume_text:
        st.error("Could not extract text from the PDF. Make sure it is not scanned/image-only.")
        st.stop()
 
    with st.spinner("🧠 Summarising your résumé with Ollama..."):
        summary = Ollama_action(
            f"Summarize this resume highlighting key skills, education and experience in clear bullet points:\n\n{resume_text}",
            max_tokens=500
        )
 
    with st.spinner("🛠️ Identifying skill gaps..."):
        skill_gaps = Ollama_action(
            f"Analyze this resume and list missing skills, certifications or experience gaps that would help the candidate land better jobs. Be specific:\n\n{resume_text}",
            max_tokens=500
        )
 
    with st.spinner("🚀 Building your career roadmap..."):
        roadmap = Ollama_action(
            f"Suggest a 6-month career roadmap for this person: skills to learn, certifications to earn, projects to build, and industry exposure to seek:\n\n{resume_text}",
            max_tokens=400
        )
 
    st.success("✅ Résumé analysis complete!")
 
    # ── Results grid ──────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns(2, gap="large")
 
    with col1:
        st.markdown("<div class='section-label'>📑 Résumé Summary</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-card'>{summary}</div>", unsafe_allow_html=True)
 
    with col2:
        st.markdown("<div class='section-label'>🛠️ Skill Gaps & Missing Areas</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-card'>{skill_gaps}</div>", unsafe_allow_html=True)
 
    st.markdown("---")
    st.markdown("<div class='section-label'>🚀 6-Month Career Roadmap</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-card'>{roadmap}</div>", unsafe_allow_html=True)
 
    # ── Job recommendations ───────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔎 Get AI-Powered Job Recommendations"):
 
        with st.spinner("📌 Extracting job keywords from your summary..."):
            keywords = Ollama_action(
                f"Based on this resume summary, give me a comma-separated list of the best job titles and search keywords. Return ONLY the comma-separated list, no explanation:\n\n{summary}",
                max_tokens=100
            )
            search_keywords_clean = keywords.replace("\n", "").strip()
 
        st.info(f"🎯 **Searching for:** {search_keywords_clean}")
 
        with st.spinner("🌐 Fetching jobs from LinkedIn & Naukri..."):
            linkedin_jobs = fetch_LinkedIn_Jobs(search_keywords_clean, rows=60)
            naukari_jobs  = fetch_Naukari_Jobs(search_keywords_clean, rows=60)
 
        st.markdown("---")
        col_li, col_nk = st.columns(2, gap="large")
 
        # ── LinkedIn jobs ─────────────────────────────────────────────────────
        with col_li:
            st.markdown("<div class='section-label'>💼 LinkedIn Jobs</div>", unsafe_allow_html=True)
            if linkedin_jobs:
                for job in linkedin_jobs:
                    st.markdown(f"""
                    <div class='job-card'>
                      <strong>{job.get('title', 'N/A')}</strong><br>
                      <span style='color:#9ca3af'>{job.get('companyName', '')}</span><br>
                      <span class='badge'>📍 {job.get('location', '')}</span><br><br>
                      <a href="{job.get('link', '#')}" target="_blank">View Job →</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No LinkedIn jobs found. Check your RapidAPI key in `src/job_api.py`.")
 
        # ── Naukri jobs ───────────────────────────────────────────────────────
        with col_nk:
            st.markdown("<div class='section-label'>🇮🇳 Naukri Jobs (India)</div>", unsafe_allow_html=True)
            if naukari_jobs:
                for job in naukari_jobs:
                    st.markdown(f"""
                    <div class='job-card'>
                      <strong>{job.get('title', 'N/A')}</strong><br>
                      <span style='color:#9ca3af'>{job.get('companyName', '')}</span><br>
                      <span class='badge'>📍 {job.get('location', '')}</span><br><br>
                      <a href="{job.get('url', '#')}" target="_blank">View Job →</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No Naukri jobs found. Check your RapidAPI key in `src/job_api.py`.")