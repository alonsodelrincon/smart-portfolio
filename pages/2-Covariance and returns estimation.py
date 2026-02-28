import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from services.ReturnsCovarianceModel import ReturnsCovarianceModel
from services.Portfolio import Portfolio
from services.PortfolioOptimizerModel import PortfolioOptimizerModel

from pages.utils.main_utils import *
from pages.utils.covariance_model_utils import *

#BASIC STREAMLIT DEFINITION

st.set_page_config(
    page_title="Definición de los métodos de estimación de varianza y retorno",
    layout='wide'
)

first_page_load = set_page(page = 2)

#CARGA DE COVARIANCE MODEL

market_data = read_key('market_data', None)

if market_data is None or not market_data.valid:
    st.error(f"Assets must be defined first!")

    delete_key('market_data')
    delete_key('returns_covariance_model')
    delete_key('portfolio_model')

    st.stop()

loaded = load_key('returns_covariance_model', lambda: default_covariance_model(market_data))

if loaded:
    delete_key('expected_return_estimation_method')
    delete_key('expected_return_bandwidth_method')
    delete_key('expected_return_bandwidth_value')
    delete_key('expected_return_lambda')

    delete_key('covariance_method')
    delete_key('covariance_bandidth_method')
    delete_key('covariance_bandidth_value')


    #  # delete_key('covariance_weighting_method')
    #  # delete_key('covariance_lambda')

    delete_key('portfolio_model')

returns_covariance_model = read_key('returns_covariance_model', None)

if returns_covariance_model is None:
    st.error(f"¡Error! Unknown error appeared, please, reset the app")
    st.stop()

#CARGA INCIAL DE WIDGETS

load_widget("expected_return_estimation_method")
load_widget("expected_return_bandwidth_method", ReturnsCovarianceModel.BandwidthMethod.ALL)
load_widget("expected_return_bandwidth_value", default_bandwidth_value(market_data=market_data)) #AQUI CHECKEAR SI 10 ES MENOR O MAYOR QUE EL RETURNS DFLENGTH
load_widget("expected_return_lambda", 0.5)

load_widget("covariance_method")
load_widget("covariance_bandidth_method")
load_widget("covariance_bandidth_value", default_bandwidth_value(market_data=market_data)) #AQUI CHECKEAR SI 10 ES MENOR O MAYOR QUE EL RETURNS DFLENGTH
# load_widget("covariance_weighting_method")
# load_widget("covariance_lambda", 0.5)

#CARGA DE RETORNOS ESTIMADOS

st.subheader("Configuración de retornos esperados")

estimation_method = st.selectbox(
    "Elige el método de estimación de retornos esperados",
    options=list(returns_covariance_model.ExpectedReturnEstimationMethod),
    format_func=lambda x: x.value,
    key="_expected_return_estimation_method",
    on_change=write_widget,
    args=["expected_return_estimation_method"]
)

bandwidth_method = None
if estimation_method not in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE):
    bandwidth_method = st.selectbox(
        "Elige el método de cálculo de bandwidth",
        options=list(returns_covariance_model.BandwidthMethod),
        format_func=lambda x: x.value,
        key="_expected_return_bandwidth_method",
        on_change=write_widget,
        args=["expected_return_bandwidth_method"]
    )

bandwidth_value = None
if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL:
    bandwidth_value = min(10, len(market_data.returns_df))

    bandwidth_value = st.number_input(
        "Select bandwidth", 
        value = "min",
        min_value = 1, 
        max_value = returns_covariance_model.market_data.returns_len,
        step = 1,
        key="_expected_return_bandwidth_value",
        on_change=write_widget,
        args=["expected_return_bandwidth_value"]
    )

expected_return_lmb = None
if estimation_method in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA):
    expected_return_lmb = st.slider(
        "Select lambda", 
        min_value = 0.1, 
        max_value = 0.9, 
        step = 0.01,
        key="_expected_return_lambda",
        on_change=write_widget,
        args=["expected_return_lambda"]
    )

returns_covariance_model.estimate_expected_returns(estimation_method = estimation_method, bandwidth_method = bandwidth_method, bandwidth_value = bandwidth_value, lmb = expected_return_lmb)

#CARGA DE MATRIZ DE COVARIANZA

st.subheader("Configuración de matriz de covarianzas")

covariance_method = st.selectbox(
    "Elige el método de estimación de la matriz de covarianzas",
    options=list(returns_covariance_model.CovarianceMethod),
    format_func=lambda x: x.value,
    key="_covariance_method",
    on_change=write_widget,
    args=["covariance_method"]
)

bandwidth_method = None
if covariance_method not in (ReturnsCovarianceModel.CovarianceMethod.SIMPLE):
    valid_bandwidth_methods = list(returns_covariance_model.BandwidthMethod)
    valid_bandwidth_methods.remove(returns_covariance_model.BandwidthMethod.ALL)

    bandwidth_method = st.selectbox(
        "Elige el método de cálculo de bandwidth",
        options=list(valid_bandwidth_methods),
        format_func=lambda x: x.value,
        key="_covariance_bandidth_method",
        on_change=write_widget,
        args=["covariance_bandidth_method"]
    )

bandwidth_value = None
if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL:
    bandwidth_value = min(10, len(market_data.returns_df))

    bandwidth_value = st.number_input(
        "Select bandwidth", 
        min_value = 1, 
        max_value = returns_covariance_model.market_data.returns_len,
        step = 1,
        key="_covariance_bandidth_value",
        on_change=write_widget,
        args=["covariance_bandidth_value"]
    )


# weighting_method = None
# if covariance_method not in (ReturnsCovarianceModel.CovarianceMethod.SIMPLE):
#     weighting_method = st.selectbox(
#         "Elige la función de weighting a usar",
#         options=list(returns_covariance_model.WeightingMethod),
#         format_func=lambda x: x.value,
#         key="_covariance_weighting_method",
#         on_change=write_widget,
#         args=["covariance_weighting_method"]
#     )

# covariance_lmb = None
# if weighting_method is not None and weighting_method in (ReturnsCovarianceModel.WeightingMethod.EXPONENTIAL):
#     covariance_lmb = st.slider(
#         "Select lambda", 
#         min_value = 0.01, 
#         max_value = 0.99, 
#         step = 0.01,
#         key="_covariance_lambda",
#         on_change=write_widget,
#         args=["covariance_lambda"]
#     )

returns_covariance_model.estimate_covariance_matrix(covariance_method=covariance_method, bandwidth_method = bandwidth_method, bandwidth_value = bandwidth_value, weighting_method = ReturnsCovarianceModel.WeightingMethod.BARLETT, lmb = None)

write_key('returns_covariance_model', returns_covariance_model)

portfolio_model = PortfolioOptimizerModel(returns_covariance_model=st.session_state.returns_covariance_model)
portfolio_model.calculate_efficient_frontier()

write_key('portfolio_model', portfolio_model)

#PLOTS

fig_cor = go.Figure(
    data=go.Heatmap(
        z=returns_covariance_model.correlation_matrix.values,
        x=[returns_covariance_model.market_data.asset_name(asset=asset) for asset in returns_covariance_model.correlation_matrix.columns],
        y=[returns_covariance_model.market_data.asset_name(asset=asset) for asset in returns_covariance_model.correlation_matrix.index],
        colorscale='Blues',
        colorbar=dict(
            len=1,
            lenmode="fraction",
            y=0.5,
            yanchor="middle"
        )
    )
)

cor, returns = st.columns([1, 1])

with cor:
    fig_cor.update_xaxes(tickangle=45, tickfont=dict(size=10))  # Rotar etiquetas X
    fig_cor.update_yaxes(tickfont=dict(size=10))               # Reducir tamaño de fuente Y
    fig_cor.update_layout(margin=dict(l=50, r=50, t=50, b=50)) # Ajustar márgenes

    fig_cor.update_layout(
        title="Matriz de Correlación",
        # xaxis_title="Activos",
        # yaxis_title="Activos",
        yaxis=dict(autorange="reversed"),
        width=600,   # ancho en píxeles
        height=600   # alto en píxeles
    )

    fig_cor.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cor, width='content')
with returns:
    fig_expected_returns = go.Figure()

    fig_expected_returns.add_trace(go.Bar(
        x=[returns_covariance_model.market_data.asset_name(asset=asset) for asset in returns_covariance_model.expected_returns.index],
        y=returns_covariance_model.expected_returns.expected_return,
        marker=dict(
            color="#3182BD"   # azul intermedio de la escala Blues
        )
    ))

    fig_expected_returns.update_layout(
        title="Retornos diarios estimados por activo",
        xaxis_title="Activos",
        yaxis_title="Retornos diarios estimados",
        template="plotly_white"
    )

    st.plotly_chart(fig_expected_returns, width='content')


with st.expander("Matriz de covarianzas"):
    fig_cov = go.Figure(
        data=go.Heatmap(
            z=returns_covariance_model.covariance_matrix.values,
            x=[returns_covariance_model.market_data.asset_name(asset=asset) for asset in returns_covariance_model.covariance_matrix.columns],
            y=[returns_covariance_model.market_data.asset_name(asset=asset) for asset in returns_covariance_model.covariance_matrix.index],
            colorscale='Blues',
            colorbar=dict(
                len=1,
                lenmode="fraction",
                y=0.5,
                yanchor="middle"
            )
        )
    )

    fig_cov.update_xaxes(tickangle=45, tickfont=dict(size=10))  # Rotar etiquetas X
    fig_cov.update_yaxes(tickfont=dict(size=10))               # Reducir tamaño de fuente Y
    fig_cov.update_layout(margin=dict(l=50, r=50, t=50, b=50)) # Ajustar márgenes

    fig_cov.update_layout(
        title="Matriz de Covarianzas diarias",
        # xaxis_title="Activos",
        # yaxis_title="Activos"
        yaxis=dict(autorange="reversed"),
        width=400,   # ancho en píxeles
        height=400   # alto en píxeles
    )

    fig_cov.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cov, width='content')  # sin use_container_width


    