import streamlit as st

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