import streamlit as st
from pages.utils.main_utils import *

st.set_page_config(
    page_title="Definición de fuentes de datos",
    layout='wide',
    initial_sidebar_state="collapsed"
)

side_menu()


init_db()

db_selector = st.selectbox(
    label="Especifica la fuente de datos a usar",
    options= DEFAULT_ASSETS_DB.keys(),
    index = list(DEFAULT_ASSETS_DB.keys()).index(st.session_state.db),
    format_func=lambda x: DEFAULT_ASSETS_DB[x]
)

set_db(db_selector)
