from show_interview_qa import show_interview_qa
from parsers.schema.interview_questions_schema import InterviewQuestionSchema
from parsers.document_parsers import parse_interview_questions
from repository.manage_session_state import manage_sessions
import streamlit as st
from data.resume_data_model import ResumeDataModel
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

manage_sessions()

if st.button("⬅ Back to resume details"):
    st.switch_page("pages/resume_details.py")

resume_data_model: ResumeDataModel = st.session_state.selected_resume_model

qaList: list[InterviewQuestionSchema] = parse_interview_questions(skills= resume_data_model.skills,
                                      experience=resume_data_model.totalExperience, summary=resume_data_model.summary)

show_interview_qa(qaList)


