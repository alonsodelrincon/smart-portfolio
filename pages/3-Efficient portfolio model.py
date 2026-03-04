import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from services.MarketData_V2 import MarketData_V2
from services.ReturnsCovarianceModel import ReturnsCovarianceModel
from services.Portfolio import Portfolio

from pages.utils.main_utils import *
from pages.utils.covariance_model_utils import *
from pages.utils.portfolio_model_utils import *

#BASIC STREAMLIT DEFINITION

side_menu()

st.set_page_config(
    page_title="Análisis de las carteras eficientes",
    layout='wide',
    initial_sidebar_state="collapsed"
)

first_page_load = set_page(page = 2)

#SPECIFIC GRAPHIC FUNCTIONS

def plot_efficient_frontier(efficient_frontier, efficient_frontier_selected_portfolio, individual_portfolios = None, custom_portfolios = None):
    portfolio_risks = [x.annual_risk for x in efficient_frontier]
    portfolio_returns = [x.annual_expected_return for x in efficient_frontier]

    selected_portfolio = efficient_frontier[efficient_frontier_selected_portfolio]

    efficient_frontier_fig = go.Figure()

    efficient_frontier_fig.add_trace(
        go.Scatter(
            x=portfolio_risks,
            y=portfolio_returns,
            mode='lines',
            name = 'Frontera eficiente'
        )
    )

    efficient_frontier_fig.add_trace(
        go.Scatter(
            x=[selected_portfolio.annual_risk],
            y=[selected_portfolio.annual_expected_return],
            mode='markers',
            marker=dict(size=10, color='blue'),
            name = 'Cartera seleccionada',
        )
    )

    if individual_portfolios is not None:
        ind_portfolio_risks = [x.annual_risk for x in individual_portfolios]
        ind_portfolio_returns = [x.annual_expected_return for x in individual_portfolios]
        ind_portfolio_names = [x.name for x in individual_portfolios]

        efficient_frontier_fig.add_trace(
            go.Scatter(
                x=ind_portfolio_risks,
                y=ind_portfolio_returns,
                mode='markers+text',
                marker=dict(size=10, color='red'),
                text=ind_portfolio_names,
                textposition="top center",
                name="Carteras de un activo"
            )
        )

    if custom_portfolios is not None:
        pers_portfolio_risks = [x.annual_risk for x in custom_portfolios]
        pers_portfolio_returns = [x.annual_expected_return for x in custom_portfolios]
        pers_portfolio_names = [x.name for x in custom_portfolios]

        efficient_frontier_fig.add_trace(
            go.Scatter(
                x=pers_portfolio_risks,
                y=pers_portfolio_returns,
                mode='markers+text',
                marker=dict(size=10, color='green'),
                text=pers_portfolio_names,
                textposition="top center",
                name="Carteras personalizadas"
            )
        )

    efficient_frontier_fig.update_layout(
        title="",
        xaxis=dict(
            title = "Riesgo anual",
            #range=[min(portfolio_risks), max(portfolio_risks)],
            #fixedrange=False  # True si quieres que no se pueda hacer zoom
        ),
        yaxis=dict(
            title = "Rentabilidad (%)",
            #range=[min(portfolio_returns), max(portfolio_returns)],
            #fixedrange=False  # True si quieres que no se pueda hacer zoom
        ),
        template="plotly_white"
    )

    st.plotly_chart(efficient_frontier_fig, width="stretch")

def plot_selected_portfolio(portfolio):
    names = portfolio.assets.asset_name

    weights = portfolio.weights

    mask = weights > 0.001

    names = names[mask]
    weights = weights[mask]

    pie_chart_fig = go.Figure()

    pie_chart_fig.add_trace(
        go.Pie(
            labels=names, 
            values=weights, 
            hole=0.0
        )
    )

    pie_chart_fig.update_traces(
        textinfo='label+percent',
        textposition='inside',           # fuerza los textos dentro de la porción
        insidetextorientation='radial'   # gira los textos para que sigan el ángulo de la porción
    )

    st.plotly_chart(pie_chart_fig, width="content")

#AQUI HABRIA QUE HACER ALGO COMO IF PORTFOLIOMODEL.RETURNS_COV_MODEL.PSD == FALSE MUESTRO UN ERROR Y PUNCH, LO MISMO EN LA OTRA PANTALLA

#CARGA DE PORTFOLIO MODEL

market_data = read_key('market_data', None)

if market_data is None or not market_data.valid:
    st.error(f"¡Error! Debes definir los activos primero")

    delete_key('market_data')
    delete_key('returns_covariance_model')

    st.stop()

returns_covariance_model = read_key('returns_covariance_model', None)

if returns_covariance_model is None:
    load_key('returns_covariance_model', lambda: default_covariance_model(market_data))
    returns_covariance_model = read_key('returns_covariance_model', None)

    delete_key('efficient_frontier_selected_portfolio')
    delete_key('efficient_frontier_n_steps')
    delete_key('portfolio_model')

    if returns_covariance_model is None:
        st.error(f"¡Error! Ha ocurrido un error desconocido, por favor, reinicia la aplicación.")

        delete_key('returns_covariance_model')

        st.stop()

loaded = load_key('portfolio_model', lambda: default_portfolio_model(returns_covariance_model))
portfolio_model = read_key('portfolio_model', None)

if portfolio_model is None:
    st.error(f"¡Error! Ha ocurrido un error desconocido, por favor, reinicia la aplicación.")
    st.stop()

if loaded:
    portfolio_model.calculate_efficient_frontier(n_steps = default_portfolio_steps()) #aqui en nsteps se puede poner el valor default con el que se cargan las keys

    #aquí podríamos cargar todos los valores de todos los portfolios

    delete_key('efficient_frontier_selected_portfolio')
    delete_key('efficient_frontier_n_steps')

#CARGA INICIAL DE WIDGETS

load_widget('efficient_frontier_selected_portfolio', 0)
load_widget('efficient_frontier_n_steps', default_portfolio_steps())

n_steps = read_key('_efficient_frontier_n_steps')
selected_portfolio = read_key('_efficient_frontier_selected_portfolio')

if selected_portfolio > n_steps:
    write_key('_efficient_frontier_selected_portfolio', 0)


efficient_frontier = portfolio_model.efficient_frontier
n_portfolios = len(efficient_frontier)

#EN EL CASO DE QUE HAYA DISCREPANCIAS ENTRE EL NÚMERO DE STEPS ESPECIFICADO Y EL DE NUESTRA FRONTERA, REDEFINIMOS LA FRONTERA
if n_steps != n_portfolios:
    portfolio_model.calculate_efficient_frontier(n_steps = n_steps)

    efficient_frontier = portfolio_model.efficient_frontier
    n_portfolios = len(efficient_frontier)

#DEFINICIÓN DE WIDGETS

st.subheader("Frontera eficiente")

efficient_frontier_selected_portfolio = st.slider(
    label = "Selecciona la cartera sobre la frontera eficiente", 
    min_value = 0, 
    max_value = n_portfolios-1, 
    step = 1,
    key="_efficient_frontier_selected_portfolio",
    on_change=write_widget,
    args=["efficient_frontier_selected_portfolio"]
)

# #EXTRAEMOS LOS PORFOLIOS INDIVIDUALES

# individual_portfolios = None
# show_individual_assets = st.checkbox("Mostrar carteras compuestas por los assets individuales")

# if show_individual_assets:
#     individual_portfolios = portfolio_model.individual_portfolios

# #AÑADIMOS UN CREADOR DE CARTERAS PERSONALIZADO

# custom_portfolio_list = None
# show_custom_portfolios = st.checkbox("Añadir carteras personalizadas")

# if show_custom_portfolios:
#     column_config = {}

#     column_config['name'] = st.column_config.TextColumn(
#         "Nombre",
#         width="small"
#     )

#     for asset in portfolio_model.assets.itertuples():
#         column_config[asset.Index] = st.column_config.NumberColumn(
#             asset.asset_name,
#             min_value=0,
#             step=1,
#             format="%d",
#             width="small"
#         )

#     columns = ['name']
#     columns.extend(portfolio_model.assets.index)

#     custom_portfolio_df = pd.DataFrame(columns=columns)
#     custom_portfolio_df.set_index('name')

#     st.caption("Configura nuevas carteras especificando su nombre y el peso de cada activo.")

#     custom_portfolio = st.data_editor(
#         custom_portfolio_df,
#         column_config=column_config,
#         num_rows="dynamic",
#         use_container_width=True
#     )

#     custom_portfolio = custom_portfolio.dropna(how="all")

#     custom_portfolio[portfolio_model.assets.index] = custom_portfolio[portfolio_model.assets.index].fillna(0)

#     tmp_portfolios = []

#     for id, portfolio in custom_portfolio.iterrows():
#         w = np.array(portfolio[portfolio_model.assets.index])

#         if sum(w) != 0:
#             w = w/sum(w)

#             tmp_portfolios.append(portfolio_model.custom_portfolio(w = w, name = portfolio['name']))

#     if len(tmp_portfolios) > 0:
#         custom_portfolio_list = tmp_portfolios

st.subheader("Carteras adicionales")

col1, col2 = st.columns(2)

with col1:
    show_individual_assets = st.toggle(
        "Activos individuales",
        help="Mostrar las carteras formadas por un único activo"
    )

with col2:
    show_custom_portfolios = st.toggle(
        "Carteras personalizadas",
        help="Crear nuevas carteras personalizadas"
    )

individual_portfolios = None
if show_individual_assets:
    individual_portfolios = portfolio_model.individual_portfolios

custom_portfolio_list = None
if show_custom_portfolios:
    column_config = {}

    column_config['name'] = st.column_config.TextColumn(
    "Nombre",
    width="small"
    )

    for asset in portfolio_model.assets.itertuples():
        column_config[asset.Index] = st.column_config.NumberColumn(
            asset.asset_name,
            min_value=0,
            step=1,
            format="%d",
            width="small"
        )

    columns = ['name']
    columns.extend(portfolio_model.assets.index)

    custom_portfolio_df = pd.DataFrame(columns=columns)
    custom_portfolio_df.set_index('name')

    st.caption(
        "Configura nuevas carteras especificando su nombre y el peso de cada activo. "
        "Los pesos se normalizarán automáticamente."
    )

    custom_portfolio = st.data_editor(
        custom_portfolio_df,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True
    )

    custom_portfolio = custom_portfolio.dropna(how="all")

    custom_portfolio[portfolio_model.assets.index] = custom_portfolio[portfolio_model.assets.index].fillna(0)

    tmp_portfolios = []

    for id, portfolio in custom_portfolio.iterrows():
        w = np.array(portfolio[portfolio_model.assets.index])

        if sum(w) != 0:
            w = w/sum(w)

            tmp_portfolios.append(portfolio_model.custom_portfolio(w = w, name = portfolio['name']))

        if len(tmp_portfolios) > 0:
            custom_portfolio_list = tmp_portfolios


frontier_col, portfolio_col = st.columns([2, 1])

#with frontier_col:
plot_efficient_frontier(efficient_frontier, efficient_frontier_selected_portfolio, individual_portfolios, custom_portfolio_list)
#with portfolio_col:

st.subheader("Cartera seleccionada")

plot_selected_portfolio(efficient_frontier[efficient_frontier_selected_portfolio])

col, _ = st.columns([1, 5])

with col:
    efficient_frontier_n_steps = st.number_input(
        "Número de carteras a calcular en la frontera eficiente",
        min_value = 2, 
        max_value = 100,
        step = 1,
        key="_efficient_frontier_n_steps",
        on_change=write_widget,
        args=["efficient_frontier_n_steps"]
    )



write_key('portfolio_model', portfolio_model)
