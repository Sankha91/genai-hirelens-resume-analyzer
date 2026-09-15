import streamlit as st
from side_bar_navigation import show_sidebar
from repository.jobDescriptions.job_description_repo import JDRepository
from repository.manage_session_state import manage_sessions
from data.jd_data_model import JDDataModel
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

show_sidebar("Job Description")

manage_sessions()

st.subheader("💼 Job Descriptions")
st.caption("View all uploaded job descriptions and their matching resumes.")

search_col, sort_col, order_col = st.columns([2.5,1.5,1])
sort_array = ["Experience", "Resumes Matched"]
order_array = ["High to low", "Low to high"]

with search_col:
    search = st.text_input(
        "Search Job Description",
        placeholder="Search by title..."
    )
with sort_col:
    sort_by = st.selectbox(
        "Sort by",
        sort_array
    )
with order_col:
    order = st.selectbox(
        "Order",
        order_array
    )
st.divider()

jdRepository: JDRepository = st.session_state.jd_repo
st.session_state.jd_data_model_list = jdRepository.fetchAllJDDetailsMain()
data_model_list: list[JDDataModel] = st.session_state.jd_data_model_list

jdRepository.sortBy(data_model_list, sort_by, order, sort_array, order_array)

if data_model_list:
    headers = st.columns([3, 2, 2, 2, 1])

    headers[0].write("**JD Title**")
    headers[1].write("**Min Experience**")
    headers[2].write("**Location**")
    headers[3].write("**Matching Resumes**")
    headers[4].write("**Action**")

    for index, jd in enumerate(data_model_list, start= 1):
        cols = st.columns([3, 2, 2, 2, 1])

        cols[0].write(jd.title)
        cols[1].write(f"{jd.minExperience} years")
        cols[2].write(jd.location)
        cols[3].write(f"{jd.totalMatchingResumes}")

        if cols[4].button("View", key=jd.id):
            st.session_state.jd_id = jd.id
            st.session_state.page = "pages/job_descriptions.py"
            st.switch_page("pages/jd_details.py")
else:
    st.info("Please come back once you upload some JDs...")