import streamlit as st
import pathlib
from pages.utils.main_utils import *

def db_change():
    write_widget('db_selection')

    reset_session()

def reset_session():
    claves_a_conservar = ["db_selection", "_db_selection", "data_path"]

    for key in list(st.session_state.keys()):
        if key not in claves_a_conservar:
            del st.session_state[key]

db_list = {
    'V1': 'Mixed funds until 24/01/2026',
    'V2': 'Indexed world, SP500 and emergin markets fund + AZVALOR + HAMCO until 24/01/2026'
}

load_widget("db_selection", list(db_list.keys())[0])


db = st.selectbox(
    label="Especifica la fuente de datos a usar",
    options= db_list.keys(),
    format_func=lambda x: db_list[x],
    key="_db_selection",
    on_change= db_change
)

current_path = pathlib.Path(__file__)
data_path = (current_path.parent / "data" / db).resolve()

write_key('data_path', data_path)


st.set_page_config(layout="wide")
