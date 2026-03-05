import streamlit as st
import pathlib
from config import DATA_DIR
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

DEFAULT_ASSETS_DB = {
    "V1": "Fondos indexados y de gestión activa 24/01/2026",
    "V2": "MSCI WORLD + SP500 + EMERGING MARKETS + AZVALOR + HAMCO 24/01/2026"
}

DEFAULT_CONFIG = {
    'db': list(DEFAULT_ASSETS_DB.keys())[0],
    'return_estimation_method': ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE,
    'return_bandwidth_method': ReturnsCovarianceModel.BandwidthMethod.ALL,
    'return_bandwidth_value': None,
    'return_lmb': None,
    'covariance_estimation_method': ReturnsCovarianceModel.CovarianceMethod.SIMPLE,
    'covariance_bandwidth_method': ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB,
    'covariance_bandwidth_value': None,
    'efficient_frontier_n_steps': None
}

#BASE_DIR = pathlib.Path(__file__).resolve().parent

def get_config():
    if 'config' not in st.session_state:
        st.write("not in")
        st.write(st.session_state)
        st.session_state.config = DEFAULT_CONFIG
        
    return st.session_state.config

def reset_session(exceptions = True):
    exceptions_list = [
        "expected_return_estimation_method",
        "expected_return_bandwidth_method",
        "expected_return_bandwidth_value",
        "expected_return_lambda",
        "covariance_method",
        "covariance_bandidth_method",
        "covariance_bandidth_value",
        "efficient_frontier_n_steps",
        "_expected_return_estimation_method",
        "_expected_return_bandwidth_method",
        "_expected_return_bandwidth_value",
        "_expected_return_lambda",
        "_covariance_method",
        "_covariance_bandidth_method",
        "_covariance_bandidth_value",
        "_efficient_frontier_n_steps",
        "config",
        "recent_page"
    ]

    # st.write("present", list(st.session_state.keys()))
    # st.write("exceptions", exceptions)
    # st.write("deleted", list(st.session_state.keys() - set(exceptions)))

    if exceptions:
        delete_list = list(st.session_state.keys() - set(exceptions_list))
    else:
        delete_list = list(st.session_state.keys())

    for key in delete_list:
        del st.session_state[key]

# def init_db():
#     if 'db' not in st.session_state:
#         reset_session()
#         db = list(DEFAULT_ASSETS_DB.keys())[0]
#         st.session_state.db = db

# def set_db(db: str):
#     if db not in DEFAULT_ASSETS_DB:
#         raise ValueError(f"{db} no es una DB válida")

#     if st.session_state.db != db:
#         reset_session()
#         st.session_state.db = db

def db_path():
    data_path = (DATA_DIR / get_config()['db']).resolve()
    return data_path

def side_menu():
    with st.sidebar:
        st.page_link('pages/config_tab.py', label="configuration", icon = "⚙️")
        st.page_link('pages/portfolio_selection_tab.py', label="portfolio selection", icon = "💹") #🧾 💹 📊
        st.page_link('pages/efficient_frontier_tab.py', label="efficient frontier", icon = "📊")

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