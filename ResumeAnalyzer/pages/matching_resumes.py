import streamlit as st
from repository.jobDescriptions.job_description_repo import JDRepository
from side_bar_navigation import show_sidebar
from repository.result.result_repo import ResultRepository
from repository.manage_session_state import manage_sessions
from data.jd_data_model import JDDataModel
from data.dashboard_data_model import DashboardDataModel
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

show_sidebar("Matching Resumes")

manage_sessions()

selected_jd_id = st.session_state.jd_id

if selected_jd_id > -1 and st.button("⬅ Back to Job Descriptions"):
    st.session_state.jd_id = -1
    st.switch_page("pages/job_descriptions.py")

st.subheader("🎯 Matching Resumes")
st.caption(
    "Explore analyzed candidates ranked by their match with the selected job description."
)

result_repo: ResultRepository = st.session_state.result_repo
jd_repo: JDRepository = st.session_state.jd_repo

if selected_jd_id == -1:
    # Directly landed on this screen from sidebar navigation
    matchesFound = result_repo.fetchTotalCount()
    data_model_list: list[DashboardDataModel] = result_repo.fetchTopNResults(matchesFound, -1)
else:
    # Redirected from JobDescription -> individual JD_Details screen
    matchesFound = result_repo.findMatchingResumesCount(selected_jd_id)
    data_model_list: list[DashboardDataModel] = result_repo.fetchTopNResults(matchesFound, selected_jd_id)

if selected_jd_id > -1:
    jd_model: JDDataModel = st.session_state.selected_jd_model
    with st.container(border=True):
        st.subheader(f"{jd_model.title}")
        st.caption(f"Min {jd_model.minExperience} years • {jd_model.location}")

highestMatch = 0

if data_model_list:
    highestMatch = int(data_model_list[0].matchPercent)

c1,c2 = st.columns(2)
with c1:
    st.metric("Candidates", matchesFound)
with c2:
    st.metric("Highest Match", f"{highestMatch}%")

search_col, sort_col, order_col, button_col = st.columns([2,1,1,1])
sort_array = ["Match Score", "Experience"]
order_array = ["High to low", "Low to high"]

with search_col:
    search = st.text_input(
        "Search Candidate...",
        placeholder="Search by name..."
    )
with sort_col:
    sort_by = st.selectbox(
        "Sort by",
        sort_array
    )
with order_col:
    order_by = st.selectbox(
        "Order by",
        order_array
    )
with button_col:

    st.write("")    # spacing and vertical alignment
   # st.write("")    # spacing and vertical alignment
    if st.button(
        "Re-analyse resumes",
        use_container_width=True,
        type="primary",
        disabled= False if selected_jd_id > -1 else True
    ):
        jd_repo.reAnalyseResumes(selected_jd_id)
        st.rerun()
st.divider()

result_repo.sortBy(data_model_list, sort_by, order_by, sort_array, order_array)

if data_model_list:

    headers = st.columns([1, 2, 2, 2, 2, 1])
    headers[0].write("**Rank**")
    headers[1].write("**Candidate**")
    headers[2].write("**Experience**")
    headers[3].write("**Skills Matched**")
    headers[4].write("**Match Score**")
    headers[5].write("**Actions**")

    for row in data_model_list:
        cols = st.columns([1, 2, 2, 2, 2, 1])

        cols[0].write(row.rank)
        cols[1].write(row.name)
        cols[2].write(row.experience)
        cols[3].write(row.skills_matched)
        with cols[4]:
            st.write(f"**{row.matchPercent}%**")
            st.progress(int(row.matchPercent) / 100)

        if cols[5].button("View", key=row.resume_id):
            st.session_state.resume_id = row.resume_id
            st.session_state.page = "pages/matching_resumes.py"
            st.switch_page("pages/resume_details.py")

else:
    st.info("It looks like you haven't analysed Resumes with Job Descriptions...")


