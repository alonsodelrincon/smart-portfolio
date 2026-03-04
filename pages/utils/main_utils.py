import streamlit as st
import pathlib
from config import DATA_DIR

DEFAULT_ASSETS_DB = {
    "V1": "Fondos indexados y de gestión activa 24/01/2026",
    "V2": "MSCI WORLD + SP500 + EMERGING MARKETS + AZVALOR + HAMCO 24/01/2026"
}

#BASE_DIR = pathlib.Path(__file__).resolve().parent

def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def init_db():
    if 'db' not in st.session_state:
        reset_session()
        db = list(DEFAULT_ASSETS_DB.keys())[0]
        st.session_state.db = db

def set_db(db: str):
    if db not in DEFAULT_ASSETS_DB:
        raise ValueError(f"{db} no es una DB válida")

    if st.session_state.db != db:
        reset_session()
        st.session_state.db = db

def db_path():
    if 'db' not in st.session_state:
        init_db()

    data_path = (DATA_DIR / st.session_state.db).resolve()
    return data_path

def side_menu():
    with st.sidebar:
        st.page_link('app.py', label="inicio", icon = "🏠")
        st.page_link('pages/1-Data selection.py', label="data", icon = "🏠")
        st.page_link('pages/config_tab.py', label="configuration", icon = "⚙️")
        st.page_link('pages/other.py', label="reset", icon = "⚙️")
        st.page_link('pages/2-Covariance and returns estimation.py', label="cov", icon = "🏠")
        st.page_link('pages/3-Efficient portfolio model.py', label="eff", icon = "🏠")

def set_page(page):
    if 'recent_page' not in st.session_state:
        st.session_state['recent_page'] = -1

    if st.session_state.recent_page == page:
        first_page_load = False
    else:
        first_page_load = True

    st.session_state['recent_page'] = page

    return first_page_load

def write_widget(key):
    st.session_state[key] = st.session_state["_"+key]

def load_widget(key, default = None):
    if key not in st.session_state:
        if default is not None:
            st.session_state["_"+key] = default
            return True
    else:
        st.session_state["_"+key] = st.session_state[key]
        return False

def write_key(key, value):
    st.session_state[key] = value

def read_key(key, default = None):
    if key not in st.session_state:
        if callable(default):
            return default()
        else:
            return default
    else:
        return st.session_state[key]

def load_key(key, default = None): 
    if key not in st.session_state:
        if callable(default):
            st.session_state[key] = default()
        else:
            st.session_state[key] = default

        return True
    
    return False

def delete_key(key):
    if key in st.session_state:
        del st.session_state[key]
        return True
    
    return False