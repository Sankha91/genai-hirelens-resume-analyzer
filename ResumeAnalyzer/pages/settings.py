from show_settings import show_settings
from side_bar_navigation import show_sidebar
from repository.manage_session_state import manage_sessions
from repository.resumes.resumes_repo import ResumeRepository
from repository.jobDescriptions.job_description_repo import JDRepository
from repository.result.result_repo import ResultRepository
import streamlit as st
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

manage_sessions()

show_sidebar("Settings")

resume_repo: ResumeRepository = st.session_state.get("resume_repo")
jd_repo: JDRepository = st.session_state.get("jd_repo")
result_repo: ResultRepository = st.session_state.get("result_repo")

show_settings(resume_repo=resume_repo, jd_repo=jd_repo, result_repo=result_repo)