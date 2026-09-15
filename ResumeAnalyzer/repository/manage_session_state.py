from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_init import SqliteDb
from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_jd import SqliteDbJD
from sqlite3_database.db_result import SqliteDbResult
from repository.resumes.resumes_repo import ResumeRepository
from repository.jobDescriptions.job_description_repo import JDRepository
from repository.result.result_repo import ResultRepository
from data.jd_data_model import JDDataModel
from data.resume_data_model import ResumeDataModel
import streamlit as st

def manage_sessions():
    if "db" not in st.session_state:
        st.session_state.db = SqliteDb()

    if "resume_repo" not in st.session_state:
        st.session_state.resume_repo = ResumeRepository(
            SqliteDbResume(st.session_state.db)
        )
    if "result_repo" not in st.session_state:
        st.session_state.result_repo = ResultRepository(
            SqliteDbResult(st.session_state.db), SqliteDbResume(st.session_state.db), SqliteDbJD(st.session_state.db)
        )
    if "jd_repo" not in st.session_state:
        st.session_state.jd_repo = JDRepository(
            st.session_state.resume_repo, SqliteDbJD(st.session_state.db), st.session_state.result_repo
        )
    if "jd_data_model_list" not in st.session_state:
        st.session_state.jd_data_model_list = []
        
    if "jd_id" not in st.session_state:
        st.session_state.jd_id = -1

    if "resume_id" not in st.session_state:
        st.session_state.resume_id = -1

    if "selected_jd_model" not in st.session_state:
        st.session_state.selected_jd_model = JDDataModel()

    if "selected_resume_model" not in st.session_state:
        st.session_state.selected_resume_model = ResumeDataModel()
        
    if "page" not in st.session_state:
        st.session_state.page = "pages/dashboard.py"