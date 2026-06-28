import streamlit as st
from src.utility_meth import extract_text_from_pdf
from src.job_api import fetch_LinkedIn_Jobs, fetch_Naukari_Jobs
from ollama_inst import Ollama_action

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("🤖AI Job Recommender")
st.markdown("Upload Your Resume and Get Job recommendations based on your skills and experience.")

upload_file = st.file_uploader("Upload your resume in (PDF)", type=["pdf"])

if upload_file:
  with st.spinner("Extracting text from your resume..."):
    resume_text = extract_text_from_pdf(pdf_path=upload_file)
  
  with st.spinner("Summarizing your resume..."):
    summary = Ollama_action(f"Summarize this resume highlighting the skills, educations and experience: \n\n{resume_text}", max_tokens=500)

  
  with st.spinner("Finding Skill Gaps..."):
    skill_gaps = Ollama_action(f"Analyze this resume and highlights missing skills, certifications and experience needed for better Job oppurtunities: \n\n {resume_text}", max_tokens=500)

  with st.spinner("Creating Future Roadmap..."):
    roadmap = Ollama_action(f"Suggest a fututre roadmap to improve this person career prospects (mention skill to learn, certification needed, industry exposure): \n\n {resume_text}", max_tokens=400)

  st.markdown("---")
  st.header("📑 Resume Summary")
  st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

  st.markdown("---")
  st.header("🛠️ Skill Gaps & Missing Areas")
  st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{skill_gaps}</div>", unsafe_allow_html=True)

  st.markdown("---")
  st.header("🚀 Future Roadmap & Preparation Strategy")
  st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

  st.success("✅ Analysis Completed Successfully!")

  if st.button("🔎Get Job Recommendation by AI🤖"):
    with st.spinner("Fetching Job Recommendations..."):
      keywords = Ollama_action(f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explainations.\n\nSummary: {summary}", max_tokens=100)

      search_keywords_clean = keywords.replace("\n","").strip()

    st.success(f"Extracted Job Keywords: {search_keywords_clean}")


    with st.spinner("Fetching Jobs from LinkedIn and Naukari..."):
      linkedin_jobs = fetch_LinkedIn_Jobs(search_keywords_clean, rows=60)
      naukari_jobs = fetch_Naukari_Jobs(search_keywords_clean, rows=60)

    
    st.markdown("---")
    st.header("🛄💰Top LinkedIn Jobs")

    if linkedin_jobs:
      for job in linkedin_jobs:
         st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
         st.markdown(f"- 📍 {job.get('location')}")
         st.markdown(f"- 🔗 [View Job]({job.get('link')})")
         st.markdown("---")
    else:
      st.warning("No LinkedIn jobs found.")

    st.markdown("---")
    st.header("💼 Top Naukri Jobs (India)")

    if naukari_jobs:
      for job in naukari_jobs:
        st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
        st.markdown(f"- 📍 {job.get('location')}")
        st.markdown(f"- 🔗 [View Job]({job.get('url')})")
        st.markdown("---")
    else:
      st.warning("No Naukri jobs found.")




