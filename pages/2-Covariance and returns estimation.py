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
    st.error(f"¡Error! Ha ocurrido un error desconocido, por favor, reinicia la aplicación.")
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

st.subheader("Rentabilidad esperada")

selector, explanation = st.columns([4, 2])

with selector:
    #st.markdown("**Método de estimación**")

    estimation_method = st.selectbox(
        "Método de estimación",
        options=list(returns_covariance_model.ExpectedReturnEstimationMethod),
        format_func=lambda x: x.value,
        key="_expected_return_estimation_method",
        on_change=write_widget,
        args=["expected_return_estimation_method"]
    )

    bandwidth_method = None
    if estimation_method not in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE):

        #st.divider()
        #st.markdown("**Número de observaciones utilizadas (bandwidth)**")

        bandwidth_method = st.selectbox(
            #"Método de estimación del *bandwidth* (número de retardos usados)"
            "Método de cálculo de número de observaciones utilizadas (bandwidth)",
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
            "Define el bandwidth", 
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
            "Selecciona $$\lambda$$ ", 
            min_value = 0.1, 
            max_value = 0.9, 
            step = 0.01,
            key="_expected_return_lambda",
            on_change=write_widget,
            args=["expected_return_lambda"]
        )


with explanation:
    if estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE:
        with st.expander("Método de estimación de rentabilidad: **Simple**", expanded=False):
            st.markdown(
                "Este método define la rentabilidad esperada del activo $i$ como "
                "$$\\hat{\\mu}_i = \\frac{1}{T} \\sum_{t=0}^{T} R_{i,t}$$."
            )
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA:
        with st.expander("Método de estimación de rentabilidad: **Exponential Moving Average**", expanded=False):
            st.markdown(
                "Este método define la rentabilidad a del activo $i$ como "
                "$$\\hat{\\mu}_i = (1-\lambda) \sum_{t=0}^{T} \lambda^{T-t} R_{i,t}$$."
            )
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_BARLETT:
        with st.expander("Método de estimación de rentabilidad: **Barlett Kernel**", expanded=False):
            st.markdown(
                "Este método define la rentabilidad a del activo $i$ como "
            )

            st.latex(r"\hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}")

            st.markdown("Donde $w_t$ es el kernel de Barlett definido como ")

            st.latex(r"w_t = \frac{t}{T}.")
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_PARZEN:
        with st.expander("Método de estimación de rentabilidad: **Parzen Kernel**", expanded=False):
            st.markdown(
                "Este método define la rentabilidad a del activo $i$ como "
            )

            st.latex(r"\hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}")

            st.markdown("Donde $w_t$ es el kernel de Parzen definido como:")

            st.markdown(r"""
            $$
            w_t =
            \begin{cases}
            1 - 6 \left( \frac{t}{T} \right)^{2} + 6 \left( \frac{t}{T} \right)^{3}, & \text{si } t \le \lfloor \frac{T}{2} \rfloor \\[2mm]
            2 \left( 1 - \frac{t}{T} \right)^{3}, & \text{si } t > \lfloor \frac{T}{2} \rfloor
            \end{cases}.
            $$
            """)
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TUKEY_HANNING:
        with st.expander("Método de estimación de rentabilidad: **Tuckey Hanning**", expanded=False):
            st.markdown(
                "Este método define la rentabilidad a del activo $i$ como "
            )

            st.latex(r"\hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}")

            st.markdown(
                "Donde $w_t$ es el kernel de Tukey-Hanning definido como:"
            )

            st.markdown(r"""
            $$
            w_t = \frac{1}{2} \left( 1 + \cos\left( \frac{\pi t}{T} \right) \right)
            $$
            """)
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TRIM:
        with st.expander("Método de estimación de rentabilidad: **Media recortada**", expanded=False):
            st.markdown(
                "La media recortada estima la rentabilidad esperada del activo $i$ "
                "como la media de las rentabilidades diarias excluyendo los percentiles extremos (por ejemplo 5% y 95%):"
            )
            st.markdown(r"""
            $$
            \hat{\mu}_i = \frac{1}{|S_i|} \sum_{t \in S_i} R_{i,t}, \quad
            S_i = \{ t : R_{i,t} \in [P_{5\%}, P_{95\%}] \}
            $$
            """)
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_WINS:
        with st.expander("Método de estimación de rentabilidad: **Media winsorizada**", expanded=False):
            st.markdown(
                "La media winsorizada define la rentabilidad esperada del activo $i$ "
                "reemplazando los extremos por los percentiles antes de calcular la media:"
            )
            st.markdown(r"""
            $$
            \hat{\mu}_i = \frac{1}{T} \sum_{t=0}^{T} \tilde{R}_{i,t}, \quad
            \tilde{R}_{i,t} = 
            \begin{cases}
            P_{5\%}, & \text{si } R_{i,t} < P_{5\%} \\
            R_{i,t}, & \text{si } P_{5\%} \le R_{i,t} \le P_{95\%} \\
            P_{95\%}, & \text{si } R_{i,t} > P_{95\%}
            \end{cases}
            $$
            """)
    elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE:
        with st.expander("Método de estimación de rentabilidad: **Estimador de media con shrinkage**", expanded=False):
            st.markdown(
                "Con shrinkage, la rentabilidad esperada se calcula combinando la media histórica de cada activo "
                "con la media global de todos los activos, ponderados por un factor $\lambda$: "
            )

            st.markdown(r"""
            $$
            \hat{\mu}_i^{\text{shrink}} = \lambda \hat{\mu}_i^{\text{hist}} + (1-\lambda) \bar{\mu}
            $$

            Donde:

            - $\hat{\mu}_i^{\text{hist}}$ es la media histórica de las renatbilidades del activo $i$  
            - $\bar{\mu}$ es la media de la rentabilidad de todos los activos  
            - $\lambda \in [0,1]$ es el factor de shrinkage
            """)

    if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
        with st.expander("### Selección del número óptimo de observaciones: **Newey–West**", expanded=False):
            st.markdown(
                "El bandwidth se calcula como:"
            )

            st.markdown(r"""
            $$
            B = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
            $$

            donde $T$ es el número total de retornos de nuestra serie.
            """)
    elif bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
        with st.expander("### Selección del número óptimo de observaciones: **Regla de Andrews**", expanded=False):
            st.markdown(
                "El bandwidth se calcula como:"
            )

            st.markdown(r"""
            $$
            B = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
            $$

            donde $T$ es el número total de retornos de nuestra serie.
            """)

returns_covariance_model.estimate_expected_returns(estimation_method = estimation_method, bandwidth_method = bandwidth_method, bandwidth_value = bandwidth_value, lmb = expected_return_lmb)

st.divider()

#CARGA DE MATRIZ DE COVARIANZA

st.subheader("Matriz de covarianzas")

selector, explanation = st.columns([4, 2])

with selector:
    #st.markdown("**Método de estimación**")

    covariance_method = st.selectbox(
        "Método de estimación",
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

        #st.divider()
        #st.markdown("**Configuración de retardos**")

        bandwidth_method = st.selectbox(
            "Método de cálculo de retardos",
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
            "Número de retardos (L)", 
            min_value = 1, 
            max_value = returns_covariance_model.market_data.returns_len,
            step = 1,
            key="_covariance_bandidth_value",
            on_change=write_widget,
            args=["covariance_bandidth_value"]
        )

with explanation:
    with st.container():
        if covariance_method == ReturnsCovarianceModel.CovarianceMethod.SIMPLE:
            #st.info("Método de estimación de la covarianza: **Simple**")
            with st.expander("Método de estimación de la covarianza: **Simple**", expanded=True):

                st.markdown(
                    "Este método considera la matriz de covarianzas $$\Sigma$$ tal que"
                )

                st.latex(r"\Sigma_{i,j} = Cov(R_i, R_j).")

            
        elif covariance_method == ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST:
            #st.info("Método de estimación de la covarianza: **Newey-West**")
            with st.expander("Método de estimación de la covarianza: **Newey-West**", expanded=True):
                st.markdown(
                    """
                    Este método estima la matriz de covarianzas teniendo en cuenta 
                    autocorrelación hasta un cierto número de retardos $$L$$.
                    """
                )

                st.latex(r"\Sigma = \sum_{t=0}^{L} w_t \, \Sigma_t.")

                st.markdown("Donde $w_t$ es el kernel de Barlett:")

                st.latex(r"w_t = \frac{L - t}{L}")

                st.markdown(
                    """
                    y $$\Sigma_{t}$$ es la matriz de covarianzas entre los retornos actuales 
                    y los retornos desplazados $$t$$ periodos.
                    """
                )

    if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
        with st.expander("### Selección del número óptimo de retardos: **Newey–West**", expanded=True):
            st.markdown(
                "El número de retardos usados se calcula como:"
            )

            st.markdown(r"""
            $$
            L = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
            $$

            donde $T$ es el número total de retornos de nuestra serie.
            """)
    elif bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
        with st.expander("### Selección del número óptimo de retardos: **Regla de Andrews**", expanded=True):
            st.markdown(
                "El número de retardos usados se calcula como:"
            )

            st.markdown(r"""
            $$
            L = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
            $$

            donde $T$ es el número total de retornos de nuestra serie.
            """)  


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

cor, returns = st.columns([1, 1])

with cor:
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
    
    fig_cor.update_xaxes(tickangle=45, tickfont=dict(size=10))  # Rotar etiquetas X
    fig_cor.update_yaxes(tickfont=dict(size=10))               # Reducir tamaño de fuente Y
    fig_cor.update_layout(margin=dict(l=50, r=50, t=50, b=50)) # Ajustar márgenes

    fig_cor.update_layout(
        title="Matriz de Correlación",
        # xaxis_title="Activos",
        # yaxis_title="Activos",
        yaxis=dict(autorange="reversed"),
        #width=600,   # ancho en píxeles
        #height=600   # alto en píxeles,
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
        title="Rentabilidad diaria estimada (%)",
        xaxis_title="Activos",
        yaxis_title="Rentabilidad (%)",
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
        yaxis=dict(autorange="reversed")
    )

    fig_cov.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cov, width='content')  # sin use_container_width


    