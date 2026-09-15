import streamlit as st
from data.jd_data_model import JDDataModel
from repository.jobDescriptions.job_description_repo import JDRepository
from repository.manage_session_state import manage_sessions
from hide_default_sidebar import hide_default_sidebar
from styles.display_skills import display_skills

hide_default_sidebar()

manage_sessions()

data_model_list: list[JDDataModel] = st.session_state.jd_data_model_list
jdRepository: JDRepository = st.session_state.jd_repo
selected_jd_id = st.session_state.jd_id

st.session_state.selected_jd_model = jdRepository.getSelectedJDModelFromList(selected_jd_id, data_model_list)
jd_model: JDDataModel = st.session_state.selected_jd_model

if st.button("⬅ Back to JD List"):
    st.session_state.jd_id = -1
    st.switch_page("pages/job_descriptions.py")
    
st.subheader("💼 Job Description Details")
st.caption(jd_model.summary)

with st.container(border=True):

        icon_col, info_col, btn_matching_resumes = st.columns([1, 6, 3])

        with icon_col:
            st.markdown("# 🏷️")

        with info_col:
            st.subheader(jd_model.title)
            st.write(f"📅 Uploaded On: {jd_model.uploadedOn}")
            st.write(f"👥 Total resumes matched: {jd_model.totalMatchingResumes}")
            st.caption(f"🕐 {jd_model.jobType.upper()} • 📍 {jd_model.location}")

        with btn_matching_resumes:
            st.write("") # Spacing
            if st.button("View Matching Resumes", type="primary"):
                st.session_state.jd_id = selected_jd_id
                st.session_state.page = "pages/jd_details.py"
                st.switch_page("pages/matching_resumes.py")

st.subheader(f"Required Skills")
with st.container(border=True):
    display_skills(jd_model.mandatorySkills)
    st.write("")

st.subheader(f"Preferred Skills")
with st.container(border=True):
    display_skills(jd_model.preferredSkills)
    st.write("")

st.subheader(f"Responsibilities")
for responsibility in jd_model.responsibility:
    st.write(f"📋 {responsibility}")