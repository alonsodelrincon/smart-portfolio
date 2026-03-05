import streamlit as st
from pages.utils.main_utils import *
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

st.set_page_config(
    page_title="Configuración",
    layout='wide',
    initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 0)

#CARGA DE TODA LA CONFIGURACION

config = get_config()

# st.write(config)

load_widget('expected_return_estimation_method', config['return_estimation_method'])
load_widget('expected_return_bandwidth_method', config['return_bandwidth_method'])
load_widget('expected_return_bandwidth_value', config['return_bandwidth_value'])
load_widget('expected_return_lambda', config['return_lmb'])

load_widget('covariance_method', config['covariance_estimation_method'])
load_widget('covariance_bandidth_method', config['covariance_bandwidth_method'])
load_widget('covariance_bandidth_value', config['covariance_bandwidth_value'])

load_widget('efficient_frontier_n_steps', config['efficient_frontier_n_steps'])

#CONFIGURACIÓN BASE DE DATOS

db_selector = st.selectbox(
    label="Especifica la fuente de datos a usar",
    options= DEFAULT_ASSETS_DB.keys(),
    index = list(DEFAULT_ASSETS_DB.keys()).index(config['db']),
    #index = list(DEFAULT_ASSETS_DB.keys()).index(st.session_state.db),
    format_func=lambda x: DEFAULT_ASSETS_DB[x]
)

st.divider()

#CONFIGURACIÓN CÁLCULO RENTABILIDAD

st.subheader("Rentabilidad esperada")

selector, explanation = st.columns([4, 2])

with selector:
    return_estimation_method = st.selectbox(
        "Método de estimación",
        
        options=list(ReturnsCovarianceModel.ExpectedReturnEstimationMethod),
        format_func=lambda x: x.value,
        key="_expected_return_estimation_method",
        on_change=write_widget,
        args=["expected_return_estimation_method"]
    )

    return_bandwidth_method = None
    if return_estimation_method not in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE):
        return_bandwidth_method = st.selectbox(
            #"Método de estimación del *bandwidth* (número de retardos usados)"
            "Método de cálculo de número de observaciones utilizadas (bandwidth)",
            options=list(ReturnsCovarianceModel.BandwidthMethod),
            format_func=lambda x: x.value,
            key="_expected_return_bandwidth_method",
            on_change=write_widget,
            args=["expected_return_bandwidth_method"]
        )

    return_bandwidth_value = None
    if return_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL:
        return_bandwidth_value = st.number_input(
            "Define el bandwidth", 
            min_value = 1,
            step = 1,
            key="_expected_return_bandwidth_value",
            on_change=write_widget,
            args=["expected_return_bandwidth_value"]
        )

    return_lmb = None
    if return_estimation_method in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA):
        return_lmb = st.slider(
            "Selecciona $$\lambda$$ ", 
            min_value = 0.1, 
            max_value = 0.9, 
            step = 0.01,
            key="_expected_return_lambda",
            on_change=write_widget,
            args=["expected_return_lambda"]
        )


with explanation:
    with st.container():
        if return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE:
            with st.expander("Método de estimación de rentabilidad: **Simple**", expanded=False):
                st.markdown(
                    "Este método define la rentabilidad esperada del activo $i$ como "
                    "$$\\hat{\\mu}_i = \\frac{1}{T} \\sum_{t=0}^{T} R_{i,t}$$."
                )
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA:
            with st.expander("Método de estimación de rentabilidad: **Exponential Moving Average**", expanded=False):
                st.markdown(
                    "Este método define la rentabilidad a del activo $i$ como "
                    "$$\\hat{\\mu}_i = (1-\lambda) \sum_{t=0}^{T} \lambda^{T-t} R_{i,t}$$."
                )
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_BARLETT:
            with st.expander("Método de estimación de rentabilidad: **Barlett Kernel**", expanded=False):
                st.markdown(
                    "Este método define la rentabilidad a del activo $i$ como "
                )

                st.latex(r"\hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}")

                st.markdown("Donde $w_t$ es el kernel de Barlett definido como ")

                st.latex(r"w_t = \frac{t}{T}.")
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_PARZEN:
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
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TUKEY_HANNING:
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
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TRIM:
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
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_WINS:
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
        elif return_estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE:
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

    with st.container():
        if return_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
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
        elif return_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
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
st.divider()

#CONFIGURACIÓN CALCULO MATRIZ DE COVARIANZA

st.subheader("Matriz de covarianzas")

selector, explanation = st.columns([4, 2])

with selector:
    covariance_estimation_method = st.selectbox(
        "Método de estimación",
        options=list(ReturnsCovarianceModel.CovarianceMethod),
        format_func=lambda x: x.value,
        key="_covariance_method",
        on_change=write_widget,
        args=["covariance_method"]
    )

    covariance_bandwidth_method = None
    if covariance_estimation_method not in (ReturnsCovarianceModel.CovarianceMethod.SIMPLE):
        valid_bandwidth_methods = list(ReturnsCovarianceModel.BandwidthMethod)
        valid_bandwidth_methods.remove(ReturnsCovarianceModel.BandwidthMethod.ALL)

        covariance_bandwidth_method = st.selectbox(
            "Método de cálculo de retardos",
            options=list(valid_bandwidth_methods),
            format_func=lambda x: x.value,
            key="_covariance_bandidth_method",
            on_change=write_widget,
            args=["covariance_bandidth_method"]
        )

    covariance_bandwidth_value = None
    if covariance_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL:
        covariance_bandwidth_value = st.number_input(
            "Número de retardos (L)", 
            min_value = 1, 
            step = 1,
            key="_covariance_bandidth_value",
            on_change=write_widget,
            args=["covariance_bandidth_value"]
        )

with explanation:
    with st.container():
        if covariance_estimation_method == ReturnsCovarianceModel.CovarianceMethod.SIMPLE:
            #st.info("Método de estimación de la covarianza: **Simple**")
            with st.expander("Método de estimación de la covarianza: **Simple**", expanded=True):

                st.markdown(
                    "Este método considera la matriz de covarianzas $$\Sigma$$ tal que"
                )

                st.latex(r"\Sigma_{i,j} = Cov(R_i, R_j).")

            
        elif covariance_estimation_method == ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST:
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

    with st.container():
        if covariance_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
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
        elif covariance_bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
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

#CONFIGURACIÓN FRONTERA EFICIENTE

efficient_frontier_n_steps = st.number_input(
    "Número de carteras a calcular en la frontera eficiente",
    min_value = 2, 
    max_value = 100,
    step = 1,
    key="_efficient_frontier_n_steps",
    on_change=write_widget,
    args=["efficient_frontier_n_steps"]
)

config = {
    'db': db_selector,
    'return_estimation_method': return_estimation_method,
    'return_bandwidth_method': return_bandwidth_method,
    'return_bandwidth_value': return_bandwidth_value,
    'return_lmb': return_lmb,
    'covariance_estimation_method': covariance_estimation_method,
    'covariance_bandwidth_method': covariance_bandwidth_method,
    'covariance_bandwidth_value': covariance_bandwidth_value,
    'efficient_frontier_n_steps': efficient_frontier_n_steps
}

if st.session_state.config != config:
    reset_session()

st.session_state.config = config