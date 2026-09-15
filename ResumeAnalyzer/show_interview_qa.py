import streamlit as st
from parsers.schema.interview_questions_schema import InterviewQuestionSchema

def show_interview_qa(qa_list: list[InterviewQuestionSchema]):
    st.subheader("🎤 Interview Q&A")
    st.caption("AI-generated interview questions based on the candidate's profile")

    # Header
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Questions", len(qa_list))

    with col2:
        technical = sum(
            1 for qa in qa_list
            if qa.category.lower() == "technical"
        )
        st.metric("Technical", technical)

    with col3:
        experience = sum(
            1 for qa in qa_list
            if qa.category.lower() == "experience"
        )
        st.metric("Experience", experience)

    with col4:
            behavioral = sum(
                1 for qa in qa_list
                if qa.category.lower() == "behavioral"
            )
            st.metric("Behavioral", behavioral)

    st.divider()

    # Category tabs
    technical_q = [
        qa for qa in qa_list
        if qa.category.lower() == "technical"
    ]

    experience_q = [
        qa for qa in qa_list
        if qa.category.lower() == "experience"
    ]

    behavioral_q = [
        qa for qa in qa_list
        if qa.category.lower() == "behavioral"
    ]

    tab1, tab2, tab3 = st.tabs(
        ["💻 Technical", "💼 Experience", "🧠 Behavioral"]
    )

    with tab1:
        render_questions(technical_q)

    with tab2:
        render_questions(experience_q)

    with tab3:
        render_questions(behavioral_q)


def render_questions(questions):

    for index, qa in enumerate(questions, start=1):

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(
                    f"**Q{index}. {qa.question}**"
                )

            with col2:
                st.caption(qa.difficulty)

            with st.expander("View Answer"):

                st.markdown("### Expected Answer")

                st.write(qa.answer)