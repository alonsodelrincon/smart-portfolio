import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from pages.utils.main_utils import *
from pages.utils.efficient_frontier_utils import *

st.set_page_config(
    page_title="Selección del portfolio",
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 3)

#CARGA DE TODA LA CONFIGURACION

config = get_config()

# st.write(config)

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

#CARGA DE PORTFOLIO MODEL

if 'returns_covariance_model' not in st.session_state:
    st.error(f"¡Error! Debes definir los activos primero")
    st.stop()

returns_covariance_model = st.session_state.returns_covariance_model

loaded = load_key('portfolio_model', lambda: default_portfolio_model(returns_covariance_model))

portfolio_model = st.session_state.portfolio_model

if loaded:
    portfolio_model.calculate_efficient_frontier(n_steps = get_config()['efficient_frontier_n_steps'])

    delete_key('efficient_frontier_selected_portfolio')

    st.session_state.portfolio_model = portfolio_model

#CARGA DE WIDGETS

load_widget('efficient_frontier_selected_portfolio', 0)

#CARGA DE LA FRONTERA EFICIENTE

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

col1, col2, col3 = st.columns([1,2,1])

with col2:
    plot_selected_portfolio(efficient_frontier[efficient_frontier_selected_portfolio])