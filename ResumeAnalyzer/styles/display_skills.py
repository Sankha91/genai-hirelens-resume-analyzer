import streamlit as st

def display_skills(skills: list[str]):
    skill_html = "".join(
        f'<span class="skill-tile">{skill}</span>'
        for skill in skills
    )

    st.markdown(
        f"""
        <div class="skills-container">
            {skill_html}
        </div>

        <style>
            .skills-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }}

            .skill-tile {{
                padding: 5px 10px;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                background-color: #f7f7f7;
                font-size: 13px;
                color: #333;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )