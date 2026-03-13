import streamlit as st
from config import DATA_DIR
from config import DEFAULT_ASSETS_DB
from services.ReturnsCovarianceModel import ReturnsCovarianceModel


DEFAULT_CONFIG = {
    'db': list(DEFAULT_ASSETS_DB.keys())[0],
    'return_estimation_method': ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE,
    'return_bandwidth_method': ReturnsCovarianceModel.BandwidthMethod.ALL,
    'return_bandwidth_value': None,
    'return_lmb': None,
    'covariance_estimation_method': ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST,
    'covariance_bandwidth_method': ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB,
    'covariance_bandwidth_value': None,
    'efficient_frontier_n_steps': 20
}

def get_config():
    if 'config' not in st.session_state:
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

    if exceptions:
        delete_list = list(st.session_state.keys() - set(exceptions_list))
    else:
        delete_list = list(st.session_state.keys())

    for key in delete_list:
        del st.session_state[key]

def db_path():
    data_path = (DATA_DIR / get_config()['db']).resolve()
    return data_path

def side_menu():
    with st.sidebar:
        st.page_link('app.py', label="Inicio", icon = "🏠")
        st.page_link('pages/config_tab.py', label="Configuración", icon = "⚙️")
        st.page_link('pages/portfolio_selection_tab.py', label="Selección de activos", icon = "💹") #🧾 💹 📊
        st.page_link('pages/efficient_frontier_tab.py', label="Frontera eficiente", icon = "📊")

def footer():
    st.divider()

    st.markdown("""
    <div style="text-align:center; font-family:monospace; font-size:12px; color:gray;">
        Creado por: Alonso del Rincón Loza 
        <a href="https://www.linkedin.com/in/alonso-del-rincón-409600344" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v10/icons/linkedin.svg" width="24" style="margin-right:8px;">
        </a>
        <a href="https://github.com/alonsodelrincon" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v10/icons/github.svg" width="24">
        </a>
        <a href="https://alonsodelrincon.com/projects.html" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/globe.svg" width="24">
        </a>
    </div>
    """, unsafe_allow_html=True)

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