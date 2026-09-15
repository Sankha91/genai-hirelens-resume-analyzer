import streamlit as st
from side_bar_navigation import show_sidebar
from hide_default_sidebar import hide_default_sidebar

hide_default_sidebar()

show_sidebar("HireLens")

st.switch_page("pages/dashboard.py")

