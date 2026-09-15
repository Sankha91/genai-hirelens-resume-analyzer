import streamlit as st
from side_bar_navigation import show_sidebar
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

show_sidebar("Recruiter AI Agent")

st.subheader("🤖 Recruiter AI Agent")
st.caption("Welcome to the Recruiter AI Agent! This tool is designed to assist recruiters in evaluating candidates based on their resumes and job descriptions. You can upload resumes and job descriptions, and the AI agent will provide insights and recommendations.")

st.info("Coming Soon!")