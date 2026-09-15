import streamlit as st
from parsers.schema.skill_gap_analysis_schema import SkillGapAnalysisListSchema


def show_skill_gap_analysis(skill_data: SkillGapAnalysisListSchema):

    if st.button("⬅ Back to resume details"):
        st.switch_page(st.session_state.page)
    st.subheader("🎯 Skill Gap Analysis")

    st.caption(
        "Compare candidate skills against the requirements of the selected job."
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    total = len(skill_data.skillGaps)

    matched = sum(
        1 for skill in skill_data.skillGaps
        if skill.status.lower() == "matched"
    )

    partial = sum(
        1 for skill in skill_data.skillGaps
        if skill.status.lower() == "partial"
    )

    missing = sum(
        1 for skill in skill_data.skillGaps
        if skill.status.lower() == "missing"
    )

    coverage = round((matched + (partial * 0.5)) / total * 100) if total else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Skill Coverage", f"{coverage}%")

    with col2:
        st.metric("Matched", matched)

    with col3:
        st.metric("Partial", partial)

    with col4:
        st.metric("Missing", missing)

    st.divider()

    # ---------------------------------------------------------
    # Skill Coverage
    # ---------------------------------------------------------

    st.subheader("Skill Coverage")

    st.progress(coverage / 100)

    st.caption(
        f"Candidate covers approximately {coverage}% "
        "of the required skills."
    )

    st.divider()

    # ---------------------------------------------------------
    # Skill Summary
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✓ Strong Skills")

        strong_skills = [
            skill for skill in skill_data.skillGaps
            if skill.status.lower() == "matched"
        ]

        for skill in strong_skills:
            st.markdown(
                f"**✓ {skill.skill_name}**  \n"
                f"{skill.candidate_skill_level}"
            )

    with col2:
        st.markdown("### ⚠ Partial Skills")

        partial_skills = [
            skill for skill in skill_data.skillGaps
            if skill.status.lower() == "partial"
        ]

        for skill in partial_skills:
            st.markdown(
                f"**⚠ {skill.skill_name}**  \n"
                f"Required: {skill.required_skill_level}  \n"
                f"Candidate: {skill.candidate_skill_level}"
            )

    with col3:
        st.markdown("### ✕ Missing Skills")

        missing_skills = [
            skill for skill in skill_data.skillGaps
            if skill.status.lower() == "missing"
        ]

        for skill in missing_skills:
            st.markdown(
                f"**✕ {skill.skill_name}**  \n"
                f"Required: {skill.required_skill_level}"
            )

    st.divider()

    # ---------------------------------------------------------
    # Detailed Comparison
    # ---------------------------------------------------------

    st.subheader("Skill Comparison")

    for skill in skill_data.skillGaps:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [2.5, 2, 2, 1.5]
            )

            with col1:
                st.markdown(f"**{skill.skill_name}**")

            with col2:
                st.caption("Required")
                st.write(skill.required_skill_level)

            with col3:
                st.caption("Candidate")
                st.write(skill.candidate_skill_level)

            with col4:
                st.caption("Gap Score")

                if skill.status.lower() == "matched":
                    st.write(f"✓ Score: {skill.gap_percent}%")

                elif skill.status.lower() == "partial":
                    st.write(f"⚠ Score: {skill.gap_percent}%")

                else:
                    st.write(f"✕ Score: {skill.gap_percent}%")

    st.divider()

    # ---------------------------------------------------------
    # AI Insight
    # ---------------------------------------------------------

    st.subheader("💡 AI Insight")

    st.info(skill_data.recommendation)
