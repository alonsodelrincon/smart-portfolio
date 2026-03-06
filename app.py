import streamlit as st
from pages.utils.main_utils import *
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

st.set_page_config(
    page_title="Inicio",
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 0)

st.header("Bienvenido a mi app")