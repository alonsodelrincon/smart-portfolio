import streamlit as st
from pages.utils.main_utils import *
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

st.set_page_config(
    page_title="reset",
    layout='wide',
    initial_sidebar_state="collapsed"
)

side_menu()