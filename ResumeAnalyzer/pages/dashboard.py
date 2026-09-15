import streamlit as st
from hide_default_sidebar import hide_default_sidebar
from data.dashboard_data_model import DashboardDataModel
from side_bar_navigation import show_sidebar
from repository.manage_session_state import manage_sessions

hide_default_sidebar()

show_sidebar("Dashboard")

manage_sessions()

st.subheader("🏠 Dashboard")
st.caption(
    "Upload resumes and job description to find the best matches."
)

left, right = st.columns(2)

with left:
    st.subheader("1. Upload Resumes")
    uploaded_files = st.file_uploader(label="Upload resume in .pdf format", type=["pdf"], 
                                      accept_multiple_files=True)
    if st.button("Save & Process All Resumes", use_container_width=True ,type="primary"):
        st.session_state.resume_repo.upload(uploaded_files)

with right:
    st.subheader("2. Job Description")
    jd_input = st.text_area(
    "Paste Job Description", height=220
    )
    if st.button("Analyze Candidates", use_container_width=True, type="primary"):
        st.session_state.jd_repo.upload(jd_input=jd_input)

st.divider()
st.subheader("3. Top 5 Matched Resumes")

matchesFound = st.session_state.result_repo.fetchTotalCount()
resultRows: list[DashboardDataModel] = st.session_state.result_repo.fetchTopNResults(min(matchesFound, 5), -1)
resumesUploaded = st.session_state.resume_repo.fetchTotalCount()
jdUploaded = st.session_state.jd_repo.fetchTotalCount()
highestMatch = 0
if resultRows:
    highestMatch = int(resultRows[0].matchPercent)
    headers = st.columns([1, 3, 2, 2, 2])

    headers[0].write("**Rank**")
    headers[1].write("**Candidate**")
    headers[2].write("**Experience**")
    headers[3].write("**Match %**")
    headers[4].write("**Skills Matched**")

    for item in resultRows:
        cols = st.columns([1, 3, 2, 2, 2])
        cols[0].write(item.rank)
        cols[1].write(item.name)
        cols[2].write(item.experience)
        cols[3].write(item.matchPercent)
        cols[4].write(item.skills_matched)
else:
    st.warning("Oh! No match found? May be you haven't analyzed any Resumes with Job Descriptions yet!")

st.divider()
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric(
        "Resumes Uploaded",
        resumesUploaded
    )

with c2:
    st.metric(
        "Job Descriptions",
        jdUploaded
    )

with c3:
    st.metric(
        "Matches Found",
        matchesFound
    )

with c4:
    st.metric(
        "Highest Match",
        f"{highestMatch}%"
    )