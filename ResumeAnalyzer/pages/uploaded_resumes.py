import streamlit as st
from data.resume_data_model import ResumeDataModel
from repository.resumes.resumes_repo import ResumeRepository
from repository.result.result_repo import ResultRepository
from data.dashboard_data_model import DashboardDataModel
from side_bar_navigation import show_sidebar
from hide_default_sidebar import hide_default_sidebar
from repository.manage_session_state import manage_sessions

hide_default_sidebar()

show_sidebar("Uploaded Resumes")

manage_sessions()    

resume_repo: ResumeRepository = st.session_state.resume_repo
result_repo: ResultRepository = st.session_state.result_repo
resume_data_model_list: list[ResumeDataModel] = resume_repo.fetchAllResumes()
analyzed_list: list[int] = result_repo.fetchDistinctResumeIds()
resume_repo.updateAnalyzedResumeModel(resume_data_model_list, analyzed_list)

st.subheader("📊 Uploaded Resumes")
st.caption(
    "View and manage all resumes uploaded for analysis."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Resumes", len(resume_data_model_list))

with col2:
    st.metric("Analyzed", len(analyzed_list))

with col3:
    st.metric("Pending", len(resume_data_model_list) - len(analyzed_list))

col1, col2, col3 = st.columns([2, 1, 1])
status_arr = ["All", "Analyzed", "Pending"]
sort_arr = ["Newest", "Oldest", "Name"]

with col1:
    search = st.text_input(
        "Search",
        placeholder="Search candidate..."
    )

with col2:
    status = st.selectbox(
        "Status",
        status_arr
    )

with col3:
    sort_by = st.selectbox(
        "Sort by",
        sort_arr
    )
st.divider()

resume_repo.filter(resume_data_model_list, sort_by, status, status_arr, sort_arr)

if resume_data_model_list:
    headers = st.columns([1, 2, 2, 2, 2, 1])
    headers[0].write("**Rank**")
    headers[1].write("**Candidate**")
    headers[2].write("**Role**")
    headers[3].write("**Experience**")
    headers[4].write("**Analyzed**")
    headers[5].write("**Actions**")

    for rank, row in enumerate(resume_data_model_list, start=1):
        if row.isAnalyzed:
            status = "✅"
        else:
            status = "❌"
        cols = st.columns([1, 2, 2, 2, 2, 1])
        cols[0].write(f"{rank}")
        cols[1].write(row.name)
        cols[2].write(row.currentRole)
        cols[3].write(f"{row.totalExperience} years")
        cols[4].write(status)
        if cols[5].button("View", key=row.id):
            st.session_state.resume_id = row.id
            st.session_state.page = "pages/uploaded_resumes.py"
            st.switch_page("pages/resume_details.py")

else:
    st.info("Please come back once you upload some Resumes...")
