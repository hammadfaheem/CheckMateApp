# navigation.py
import streamlit as st

def render_navigation():
    # Initialize the current page if it doesn't exist
    if "page" not in st.session_state:
        st.session_state.page = 0

    def next_page():
        st.session_state.page += 1

    def previous_page():
        st.session_state.page = max(st.session_state.page - 1, 0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            previous_page()
    with col2:
        if st.button("Next"):
            next_page()
