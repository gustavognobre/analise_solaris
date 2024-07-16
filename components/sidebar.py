# components/sidebar.py
import streamlit as st
from streamlit_option_menu import option_menu

def sidebar(title, labels):
    with st.sidebar:
        selected = option_menu(
            menu_title=title,
            options=labels,
            menu_icon="cast",
            default_index=0,
        )
    return selected
