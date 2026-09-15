import streamlit as st
from repository.result.result_repo import ResultRepository
from repository.resumes.resumes_repo import ResumeRepository
from repository.jobDescriptions.job_description_repo import JDRepository
from embedding.vector_store import reset_vector_store

def show_settings(resume_repo: ResumeRepository, jd_repo: JDRepository, result_repo: ResultRepository):

    st.subheader("⚙️ Settings")
    st.caption("Manage your Resume Analyzer data and analysis")
    total_results = 0
    total_resumes = 0
    total_jds = 0
    
    try:
        total_resumes = resume_repo.fetchTotalCount()
        total_jds = jd_repo.fetchTotalCount()
        total_results = result_repo.fetchTotalCount()
    except Exception as e:
        st.error(f"Error fetching data counts: {e}")

    # =========================================================
    # DATA MANAGEMENT
    # =========================================================

    st.markdown("## Data Management")

    # ---------------------------------------------------------
    # Delete Resumes
    # ---------------------------------------------------------

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown("### 🗑 Delete Resumes")
            st.caption(
                "Remove uploaded resumes and their candidate analysis data."
            )

            # Replace with your repository call
            resume_count = total_resumes

            st.caption(f"{resume_count} resume{'s' if resume_count != 1 else ''}")

        with col2:
            st.write("")

            if st.button(
                "Delete →",
                key="delete_resumes",
                use_container_width=True
            ):
                st.session_state["show_delete_resume"] = True


    # Confirmation
    if st.session_state.get("show_delete_resume", False):

        with st.container(border=True):

            st.warning(
                "Deleting resumes will also remove their associated "
                "matching and analysis data."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Cancel",
                    key="cancel_delete_resume",
                    use_container_width=True
                ):
                    st.session_state["show_delete_resume"] = False
                    st.rerun()

            with col2:
                if st.button(
                    "Delete Resumes",
                    key="confirm_delete_resume",
                    type="primary",
                    use_container_width=True
                ):
                    resume_repo.deleteAllResumes()
                    reset_vector_store()

                    st.session_state["show_delete_resume"] = False

                    st.success("All resumes deleted successfully.")
                    st.rerun()


    st.write("")


    # =========================================================
    # DELETE JOB DESCRIPTIONS
    # =========================================================

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown("### 🗑 Delete Job Descriptions")
            st.caption(
                "Remove uploaded job descriptions and their matching data."
            )
            st.caption(f"{total_jds} job description{'s' if total_jds != 1 else ''}")

        with col2:
            st.write("")

            if st.button(
                "Delete →",
                key="delete_jds",
                use_container_width=True
            ):
                st.session_state["show_delete_jd"] = True


    # Confirmation
    if st.session_state.get("show_delete_jd", False):

        with st.container(border=True):

            st.warning(
                "Deleting job descriptions will also remove their "
                "associated matching results."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Cancel",
                    key="cancel_delete_jd",
                    use_container_width=True
                ):
                    st.session_state["show_delete_jd"] = False
                    st.rerun()

            with col2:
                if st.button(
                    "Delete Job Descriptions",
                    key="confirm_delete_jd",
                    type="primary",
                    use_container_width=True
                ):
                    jd_repo.deleteAllJDs()
                    st.session_state["show_delete_jd"] = False

                    st.success(
                        "All job descriptions deleted successfully."
                    )
                    st.rerun()

    st.divider()


    # =========================================================
    # MATCHING RESULTS
    # =========================================================

    st.markdown("## Matching & Analysis")

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown("### 🔄 Clear Matching Results")
            st.caption(
                "Remove all resume-to-job matching results. "
                "Resumes and job descriptions will remain."
            )
            st.caption(f"{total_results} matching results")

        with col2:
            st.write("")

            if st.button(
                "Clear →",
                key="clear_matching",
                use_container_width=True
            ):
                st.session_state["show_clear_matching"] = True


    if st.session_state.get("show_clear_matching", False):

        with st.container(border=True):

            st.warning(
                "All resume ↔ job matching results will be permanently removed."
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Cancel",
                    key="cancel_clear_matching",
                    use_container_width=True
                ):
                    st.session_state["show_clear_matching"] = False
                    st.rerun()

            with col2:
                if st.button(
                    "Clear Results",
                    key="confirm_clear_matching",
                    type="primary",
                    use_container_width=True
                ):
                    result_repo.deleteAllResults()

                    st.session_state["show_clear_matching"] = False

                    st.success(
                        "Matching results cleared successfully."
                    )
                    st.rerun()


    # ---------------------------------------------------------
    # Regenerate AI Analysis
    # ---------------------------------------------------------

    st.write("")

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown("### ✨ Regenerate AI Analysis")
            st.caption(
                "Re-run AI analysis for resumes or job descriptions."
            )

        with col2:
            st.write("")

            if st.button(
                "Generate →",
                key="regenerate_ai",
                use_container_width=True
            ):
                st.switch_page("pages/job_descriptions.py")


    st.divider()


    # =========================================================
    # DANGER ZONE
    # =========================================================

    st.markdown("## ⚠ Danger Zone")

    with st.container(border=True):

        st.markdown("### 🗑 Clear All Application Data")

        st.caption(
            "Permanently delete all resumes, job descriptions, "
            "and AI-generated analysis."
        )

        st.write("")

        if st.button(
            "Delete Everything",
            key="delete_everything",
            type="primary",
            use_container_width=True
        ):
            st.session_state["show_delete_everything"] = True


    # Confirmation
    if st.session_state.get("show_delete_everything", False):

        with st.container(border=True):

            st.warning(
                """
                ⚠ This action cannot be undone.
                All resumes, job descriptions and
                AI-generated analysis will be permanently deleted.
                """
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Cancel",
                    key="cancel_delete_everything",
                    use_container_width=True
                ):
                    st.session_state["show_delete_everything"] = False
                    st.rerun()

            with col2:
                if st.button(
                    "Yes, Delete Everything",
                    key="confirm_delete_everything",
                    type="primary",
                    use_container_width=True
                ):
                    result_repo.dropResultTables()
                    jd_repo.dropJDTables()
                    resume_repo.dropResumeTables()
                    reset_vector_store()
                    
                    st.session_state["show_delete_everything"] = False

                    st.success(
                        "All application data has been deleted."
                    )

                    st.rerun()