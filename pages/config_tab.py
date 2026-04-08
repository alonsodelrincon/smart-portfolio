import streamlit as st
from pages.utils.main_utils import *
from services.SimpleReturnsCovarianceModel import SimpleReturnsCovarianceModel
from pages.utils.translations import translations_config

config = get_config()

set_page_translations(translations_config, lang=config['lang'])

st.set_page_config(
    page_title=tr("page_title"),
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 1)

#CARGA DE TODA LA CONFIGURACION

load_widget('expected_return_estimation_method', config['return_estimation_method'])
load_widget('expected_return_bandwidth_method', config['return_bandwidth_method'])
load_widget('expected_return_bandwidth_value', config['return_bandwidth_value'])
load_widget('expected_return_lambda', config['return_lmb'])

load_widget('covariance_method', config['covariance_estimation_method'])
load_widget('covariance_bandidth_method', config['covariance_bandwidth_method'])
load_widget('covariance_bandidth_value', config['covariance_bandwidth_value'])

load_widget('efficient_frontier_n_steps', config['efficient_frontier_n_steps'])

load_widget('active_bootstrap', config['active_bootstrap'])
load_widget('bootstrap_sample_size', config['bootstrap_sample_size'])
load_widget('bootstrap_block_size', config['bootstrap_block_size'])

#IDIOMA
st.header(tr("header_language"))

language_col, apply_col, _ = st.columns([4, 2, 5], vertical_alignment="bottom")

with language_col:
    language_selector = st.selectbox(
        label=tr("language_selector_label"),
        options= LANGUAGES.keys(),
        index = list(LANGUAGES.keys()).index(config['lang']),
        format_func=lambda x: LANGUAGES[x],
        #on_change=st.rerun()
    )

with apply_col:
    st.button(tr("language_apply"))

st.divider()

#CONFIGURACIÓN BASE DE DATOS
st.header(tr("header_database"))

st.markdown(tr("db_description"))

db_selector = st.selectbox(
    label=tr("db_selector_label"),
    options= DEFAULT_ASSETS_DB.keys(),
    index = list(DEFAULT_ASSETS_DB.keys()).index(config['db']),
    format_func=lambda x: DEFAULT_ASSETS_DB[x]
)

st.divider()

#CONFIGURACIÓN CÁLCULO RENTABILIDAD
st.header(tr("header_expected_return"))
st.subheader(tr("subheader_expected_return"))


selector, explanation = st.columns([4, 2])

with selector:
    valid_return_estimations = list(SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod)
    #valid_return_estimations.remove(SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE)

    return_estimation_method = st.selectbox(
        tr("select_method_expected_return"),
        options=list(valid_return_estimations),
        format_func=lambda x: x.value,
        key="_expected_return_estimation_method",
        on_change=write_widget,
        args=["expected_return_estimation_method"]
    )

    return_bandwidth_method = None
    if return_estimation_method not in (SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE):
        return_bandwidth_method = st.selectbox(
            #"Método de estimación del *bandwidth* (número de retardos usados)"
            tr("select_bandwidth_method"),
            options=list(SimpleReturnsCovarianceModel.BandwidthMethod),
            format_func=lambda x: x.value,
            key="_expected_return_bandwidth_method",
            on_change=write_widget,
            args=["expected_return_bandwidth_method"]
        )

    return_bandwidth_value = None
    if return_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.MANUAL:
        return_bandwidth_value = st.number_input(
            tr("input_bandwidth_value"),
            min_value = 1,
            step = 1,
            key="_expected_return_bandwidth_value",
            on_change=write_widget,
            args=["expected_return_bandwidth_value"]
        )

    return_lmb = None
    if return_estimation_method in (SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE, SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA):
        return_lmb = st.slider(
            tr("slider_lambda"),
            min_value = 0.1, 
            max_value = 0.9, 
            step = 0.01,
            key="_expected_return_lambda",
            on_change=write_widget,
            args=["expected_return_lambda"]
        )


with explanation:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        if return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE:
            with st.expander(tr("expander_simple"), expanded=False):
                st.markdown(tr("expander_simple_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA:
            with st.expander(tr("expander_ewma"), expanded=False):
                st.markdown(tr("expander_ewma_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_BARLETT:
            with st.expander(tr("expander_barlett"), expanded=False):
                st.markdown(tr("expander_barlett_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_PARZEN:
            with st.expander(tr("expander_parzen"), expanded=False):
                st.markdown(tr("expander_parzen_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TUKEY_HANNING:
            with st.expander(tr("expander_tuckey"), expanded=False):
                st.markdown(tr("expander_tuckey_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TRIM:
            with st.expander(tr("expander_trim"), expanded=False):
                st.markdown(tr("expander_trim_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_WINS:
            with st.expander(tr("expander_wins"), expanded=False):
                st.markdown(tr("expander_wins_text"))

        elif return_estimation_method == SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE:
            with st.expander(tr("expander_shrinkage"), expanded=False):
                st.markdown(tr("expander_shrinkage_text"))

    with st.container():
        if return_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
            with st.expander(tr("expander_newey_west_bandwidth"), expanded=False):
                st.markdown(tr("expander_newey_west_bandwidth_text"))

        elif return_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
            with st.expander(tr("expander_andrews_plugin_bandwidth"), expanded=False):
                st.markdown(tr("expander_andrews_plugin_bandwidth_text"))

st.write("")
st.write("")
st.write("")

#CONFIGURACIÓN CALCULO MATRIZ DE COVARIANZA
st.subheader(tr("subheader_covariance_matrix"))

selector, explanation = st.columns([4, 2])

with selector:
    covariance_estimation_method = st.selectbox(
        tr("select_method_covariance"),
        options=list(SimpleReturnsCovarianceModel.CovarianceMethod),
        format_func=lambda x: x.value,
        key="_covariance_method",
        on_change=write_widget,
        args=["covariance_method"]
    )

    covariance_bandwidth_method = None
    if covariance_estimation_method not in (SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE):
        valid_bandwidth_methods = list(SimpleReturnsCovarianceModel.BandwidthMethod)
        valid_bandwidth_methods.remove(SimpleReturnsCovarianceModel.BandwidthMethod.ALL)

        covariance_bandwidth_method = st.selectbox(
            tr("select_cov_bandwidth_method"),
            options=list(valid_bandwidth_methods),
            format_func=lambda x: x.value,
            key="_covariance_bandidth_method",
            on_change=write_widget,
            args=["covariance_bandidth_method"]
        )

    covariance_bandwidth_value = None
    if covariance_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.MANUAL:
        covariance_bandwidth_value = st.number_input(
            tr("input_cov_bandwidth_value"),
            min_value = 1, 
            step = 1,
            key="_covariance_bandidth_value",
            on_change=write_widget,
            args=["covariance_bandidth_value"]
        )

with explanation:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        if covariance_estimation_method == SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE:
            with st.expander(tr("expander_cov_simple"), expanded=True):
                st.markdown(tr("expander_cov_simple_text"))

        elif covariance_estimation_method == SimpleReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST:
            with st.expander(tr("expander_cov_newey"), expanded=True):
                st.markdown(tr("expander_cov_newey_text"))

    with st.container():
        if covariance_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
            with st.expander(tr("expander_newey_west_lags"), expanded=True):
                st.markdown(tr("expander_newey_west_lags_text"))

        elif covariance_bandwidth_method == SimpleReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
            with st.expander(tr("expander_andrews_plugin_lags"), expanded=True):
                st.markdown(tr("expander_andrews_plugin_lags_text"))

st.divider()

#CONFIGURACIÓN FRONTERA EFICIENTE
st.header(tr("header_efficient_frontier"))

efficient_frontier_n_steps = st.number_input(
    tr("input_efficient_n_steps"),
    min_value = 2, 
    max_value = 100,
    step = 1,
    key="_efficient_frontier_n_steps",
    on_change=write_widget,
    args=["efficient_frontier_n_steps"]
)

st.divider()

#CONFIGURACION BOOTSTRAP

st.header(tr("bootstrap_config"))

active_bootstrap = st.toggle(
    tr("apply_bootstrapping"),
    key="_active_bootstrap",
    on_change=write_widget,
    args=["active_bootstrap"])

bootstrap_sample_size = None
bootstrap_block_size = None

if active_bootstrap:
    bootstrap_sample_size = st.number_input(
        tr("sample_size"),
        min_value = 50, 
        max_value = 1000,
        step = 1,
        key="_bootstrap_sample_size",
        on_change=write_widget,
        args=["bootstrap_sample_size"]
    )

    bootstrap_block_size = st.number_input(
        tr("block_size"),
        min_value = 10, 
        max_value = 200,
        step = 1,
        key="_bootstrap_block_size",
        on_change=write_widget,
        args=["bootstrap_block_size"]
    )

config = {
    'db': db_selector,
    'lang': language_selector,
    'return_estimation_method': return_estimation_method,
    'return_bandwidth_method': return_bandwidth_method,
    'return_bandwidth_value': return_bandwidth_value,
    'return_lmb': return_lmb,
    'covariance_estimation_method': covariance_estimation_method,
    'covariance_bandwidth_method': covariance_bandwidth_method,
    'covariance_bandwidth_value': covariance_bandwidth_value,
    'efficient_frontier_n_steps': efficient_frontier_n_steps,

    'active_bootstrap': active_bootstrap,
    'bootstrap_sample_size': bootstrap_sample_size,
    'bootstrap_block_size': bootstrap_block_size
}

if st.session_state.config != config:
    reset_session()

st.session_state.config = config

footer()