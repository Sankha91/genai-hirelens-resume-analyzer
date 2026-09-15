from show_skill_gap_analysis import show_skill_gap_analysis
from repository.resumes.resumes_repo import ResumeRepository
from repository.jobDescriptions.job_description_repo import JDRepository
from parsers.schema.skill_gap_analysis_schema import SkillGapAnalysisListSchema
from parsers.document_parsers import parse_skill_gap_analysis
from data.resume_data_model import ResumeDataModel
from data.jd_data_model import JDDataModel
from repository.manage_session_state import manage_sessions
import streamlit as st
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

manage_sessions()

resume_repo: ResumeRepository = st.session_state.get("resume_repo")
jd_repo: JDRepository = st.session_state.get("jd_repo")
selected_jd_id = st.session_state.get("jd_id")
selected_resume_id = st.session_state.get("resume_id")
jd_data_model: JDDataModel = st.session_state.get("selected_jd_model")
resume_data_model: ResumeDataModel = st.session_state.get("selected_resume_model")

if not resume_data_model:
    resume_data_model: ResumeDataModel = resume_repo.fetchResumeDetailsFromId(selected_resume_id)
    st.session_state.selected_resume_model = resume_data_model

skill_gap_analysis_list: SkillGapAnalysisListSchema = parse_skill_gap_analysis(
    jd_mandatory_skills=jd_data_model.mandatorySkills,
    jd_preferred_skills=jd_data_model.preferredSkills,
    candidate_skills=resume_data_model.skills,
    projects=resume_data_model.projects,
    certifications=resume_data_model.certifications,
    candidate_summary=resume_data_model.summary,
    domain_expertise=resume_data_model.domainExpertise,
)
show_skill_gap_analysis(skill_data=skill_gap_analysis_list)




