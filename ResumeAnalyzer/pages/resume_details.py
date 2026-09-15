import streamlit as st
from repository.manage_session_state import manage_sessions 
from repository.resumes.resumes_repo import ResumeRepository
from repository.result.result_repo import ResultRepository
from data.resume_data_model import ResumeDataModel
from data.result_data_model import ResultDataModel
from styles.display_skills import display_skills
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

manage_sessions()

if st.button("⬅ Back to Resumes"):
    st.switch_page("pages/matching_resumes.py")

st.subheader("👤 Candidate Details")

selected_resume_id = st.session_state.resume_id
selected_jd_id = st.session_state.jd_id
resume_respository: ResumeRepository = st.session_state.resume_repo
data_model: ResumeDataModel = resume_respository.fetchResumeDetailsFromId(selected_resume_id)
st.session_state.selected_resume_model = data_model

if selected_jd_id > -1:
    # If navigating from JD_Details -> View matching Resumes
    result_repo: ResultRepository = st.session_state.result_repo
    result_data_model: ResultDataModel = result_repo.fetchResumeDetailsFromIds(resumeId=selected_resume_id, jdId=selected_jd_id)

# Header Card
with st.container(border=True):
    profile_col, info_col = st.columns([1, 9])
    with profile_col:
        st.markdown(
        "<h1 style='text-align:center;'>👤</h1>",
        unsafe_allow_html=True
        )

    with info_col:
        st.subheader(data_model.name)
        st.caption(data_model.currentRole)
        contact1, contact2, contact3 = st.columns(3)
        with contact1:
            st.write(f"✉ {data_model.email}")
        with contact2:
            st.write(f"📞 {data_model.phone}")
        with contact3:
            st.write(f"📍 {data_model.location}")
        st.write(f"**Total Experience:** {data_model.totalExperience} years")

# Summary
st.markdown("#### 📝 Professional Summary")
summary = f"""{data_model.summary}"""
with st.container(border=True):
    st.write(summary)

# Score Row
if selected_jd_id > -1:
    left_col, right_col = st.columns([1, 1])
    with left_col:
        with st.container(border=True):
            st.write("**Overall Match Score**")
            st.caption("This score indicates how well the candidate's skills and experience align with the job requirements.")
            st.markdown(
                f"<h3 style='text-align:center;'>{result_data_model.matchPercent}%</h3>",
                unsafe_allow_html=True
            )
            st.progress(result_data_model.matchPercent)
            if result_data_model.matchPercent >= 70:
                st.success("Excellent Match - Candidate is highly suitable for the interview.")
            elif result_data_model.matchPercent > 50 and result_data_model.matchPercent < 70:
                st.warning("Average Match - Candidate has some relevant skills but may need improvement.")
            else:
                st.error("Poor Match - Candidate lacks the required skills and experience for the interview.")
    with right_col:
        with st.container(border=True):
            st.write("💪 **Strengths**")
            st.write(f"• {result_data_model.strengths}")
            st.divider()
            st.write("⚠️ **Weaknesses**")
            st.write(f"• {result_data_model.weakness}")
    
# Skills Row
if selected_jd_id > -1:
    left_col, right_col = st.columns(2)
    matching_skills = result_data_model.matchingSkills
    with left_col:
        with st.container(border=True):
            st.markdown("##### ✅ Matching Skills")
            st.caption("These are the skills that the candidate possesses and match the job requirements.")
            for skill in matching_skills:
                st.write(f"✔ {skill}")

    missing_skills = result_data_model.missingSkills
    with right_col:
        with st.container(border=True):
            st.markdown("##### ❌ Missing Skills")
            st.caption("These are the skills that the candidate lacks based on the job requirements.")
            for skill in missing_skills:
                st.write(f"• {skill}")
else:
    st.markdown("#### ✅ Skills")
    with st.container(border=True):
        display_skills(data_model.skills) 
        st.write("") # extra spacing   

# Projects
st.markdown("#### 📂 Projects")
projects = data_model.projects
with st.container(border=True):
    if projects:
        for project in projects:
            st.write(f"→ {project}")
    else:
        st.info("No projects available.")

# Education and Certification
st.markdown("#### 🎓 Education & Certifications")

education = data_model.education
certifications = data_model.certifications

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🎓 Education")
        if education:
            for edu in education:
                st.write(f"• {edu}")
        else:
            st.caption("No education details mentioned.")

    with col2:
        st.markdown("##### 📜 Certifications")
        if certifications:
            for cert in certifications:
                st.write(f"→ {cert}")
        else:
            st.caption("No certifications mentioned.")

with st.container(border=True):
    if selected_jd_id > -1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ❓Suggested Interview Questions")
            st.caption("AI-generated questions based on candidate's skills and experience")
            if st.button("View Interview Questions"):
                st.session_state.page = "pages/resume_details.py"
                st.switch_page("pages/interview_questions.py")
        with col2:
            st.markdown("####  🎯 Skill Gap Analysis")
            st.caption("Identify missing and weak skills against the job requirements.")
            if st.button("View Full Analysis"):
                st.session_state.page = "pages/resume_details.py"
                st.switch_page("pages/skill_gap_analysis.py")
    else:
        st.markdown("#### ❓Suggested Interview Questions")
        st.caption("AI-generated questions based on candidate's skills and experience")
        if st.button("View Interview Questions"):
            st.session_state.page = "pages/resume_details.py"
            st.switch_page("pages/interview_questions.py")