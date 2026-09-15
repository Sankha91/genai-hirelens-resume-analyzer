import streamlit as st

def show_sidebar(pageTitle: str):
    st.set_page_config(
        page_title=pageTitle,
        page_icon="🔍",
        layout="wide"
    )
    with st.sidebar:
        st.title("🔍 HireLens")
        st.page_link(
            "pages/dashboard.py",
            label="Dashboard",
            icon="🏠"
        )
        st.page_link(
            "pages/job_descriptions.py",
            label="Job Descriptions",
            icon="💼"
        )
        st.page_link(
            "pages/matching_resumes.py",
            label="Matching Resumes",
            icon="🎯"
        )
        st.page_link(
            "pages/uploaded_resumes.py",
            label="Uploaded Resumes",
            icon="📊"
        )
        st.page_link(
            "pages/recruiter_ai_agent.py",
            label="Recruiter AI Agent",
            icon="🤖"
        )
        st.page_link(
            "pages/settings.py",
            label="Settings",
            icon="⚙️"
        )
