import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pages.utils.main_utils import *
from pages.utils.translations import translations_efficient_frontier

set_page_translations(translations_efficient_frontier, lang=get_config()['lang'])

st.set_page_config(
    page_title=tr("page_title"),
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 3)

#SPECIFIC GRAPHIC FUNCTIONS

def plot_efficient_frontier(efficient_frontier, efficient_frontier_selected_portfolio, individual_portfolios = None, custom_portfolios = None, bootstrap_efficient_frontier = None):
    portfolio_risks = [x.annual_risk for x in efficient_frontier]
    portfolio_returns = [x.annual_expected_return for x in efficient_frontier]

    selected_portfolio = efficient_frontier[efficient_frontier_selected_portfolio]

    efficient_frontier_fig = go.Figure()

    efficient_frontier_fig.add_trace(
        go.Scatter(
            x=portfolio_risks,
            y=portfolio_returns,
            mode='lines',
            marker=dict(color='blue'),
            name = tr("trace_frontier")
        )
    )

    efficient_frontier_fig.add_trace(
        go.Scatter(
            x=[selected_portfolio.annual_risk],
            y=[selected_portfolio.annual_expected_return],
            mode='markers',
            marker=dict(size=10, color='blue'),
            name = tr("trace_selected_portfolio")
        )
    )

    if bootstrap_efficient_frontier is not None:
        bootstrap_portfolio_risks = [x.annual_risk for x in bootstrap_efficient_frontier]
        bootstrap_portfolio_returns = [x.annual_expected_return for x in bootstrap_efficient_frontier]

        bootstrap_selected_portfolio = bootstrap_efficient_frontier[efficient_frontier_selected_portfolio]

        efficient_frontier_fig.add_trace(
            go.Scatter(
                x=bootstrap_portfolio_risks,
                y=bootstrap_portfolio_returns,
                mode='lines',
                marker=dict(color='gray'),
                name = tr("trace_frontier_bootstrap")
            )
        )

        efficient_frontier_fig.add_trace(
            go.Scatter(
                x=[bootstrap_selected_portfolio.annual_risk],
                y=[bootstrap_selected_portfolio.annual_expected_return],
                mode='markers',
                marker=dict(size=10, color='gray'),
                name = tr("trace_selected_portfolio_bootstrap")
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
                name=tr("trace_individual_portfolios")
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
                name=tr("trace_custom_portfolios")
            )
        )

    margin = 0.1
    risk_range = max(portfolio_risks) - min(portfolio_risks)
    return_range = max(portfolio_returns) - min(portfolio_returns)

    efficient_frontier_fig.update_layout(
        title="",
        xaxis=dict(
            title = tr("xaxis_risk"),
            #range=[min(portfolio_risks) - risk_range*margin, max(portfolio_risks) + risk_range*margin],
            fixedrange=False
        ),
        yaxis=dict(
            title = tr("yaxis_return"),
            #range=[min(portfolio_returns) - return_range*margin, max(portfolio_returns) + return_range*margin],
            fixedrange=False
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
        textposition='inside',           # TEXTOS DENTRO DEL QUESITO
        insidetextorientation='radial'
    )

    st.plotly_chart(pie_chart_fig, width="content")

#CARGA DE PORTFOLIO MODEL Y EFFICIENT FRONTIER

if 'main_pipeline' not in st.session_state or (get_config()['active_bootstrap'] and 'bootstrap_pipeline' not in st.session_state):
    st.error(tr("error_assets_not_defined"))
    st.stop()

main_pipeline = st.session_state.main_pipeline

main_pipeline.calculate_efficient_frontier(n_steps = get_config()['efficient_frontier_n_steps'])

st.session_state.main_pipeline = main_pipeline

efficient_frontier = main_pipeline.efficient_frontier

n_portfolios = len(efficient_frontier)

bootstrap_efficient_frontier = None
if get_config()['active_bootstrap']:
    bootstrap_pipeline = st.session_state.bootstrap_pipeline

    bootstrap_pipeline.calculate_efficient_frontier(n_steps = get_config()['efficient_frontier_n_steps'])

    st.session_state.bootstrap_pipeline = bootstrap_pipeline

    bootstrap_efficient_frontier = bootstrap_pipeline.efficient_frontier

#CARGA DE WIDGETS

load_widget('efficient_frontier_selected_portfolio', 0)

#DEFINICIÓN DE WIDGETS

st.subheader(tr("subheader_frontier"))

st.markdown(tr("frontier_description_1"))

st.markdown(tr("frontier_description_2"))

efficient_frontier_selected_portfolio = st.slider(
    label = tr("slider_selected_portfolio"), 
    min_value = 0, 
    max_value = n_portfolios-1, 
    step = 1,
    key="_efficient_frontier_selected_portfolio",
    on_change=write_widget,
    args=["efficient_frontier_selected_portfolio"]
)


st.subheader(tr("subheader_additional_portfolios"))

col1, col2 = st.columns(2)

with col1:
    show_individual_assets = st.toggle(
        tr("toggle_individual_assets"),
        help=tr("toggle_individual_assets_help")
    )

with col2:
    show_custom_portfolios = st.toggle(
        tr("toggle_custom_portfolios"),
        help=tr("toggle_custom_portfolios_help")
    )

individual_portfolios = None
if show_individual_assets:
    individual_portfolios = main_pipeline.individual_portfolios

custom_portfolio_list = None
if show_custom_portfolios:
    column_config = {}

    column_config['name'] = st.column_config.TextColumn(
    tr("custom_portfolio_column_name"),
    width="small"
    )

    for asset in main_pipeline.assets.itertuples():
        column_config[asset.Index] = st.column_config.NumberColumn(
            asset.asset_name,
            min_value=0,
            step=1,
            format="%d",
            width="small"
        )

    columns = ['name']
    columns.extend(main_pipeline.assets.index)

    custom_portfolio_df = pd.DataFrame(columns=columns)
    custom_portfolio_df.set_index('name')

    st.caption(tr("custom_portfolio_caption"))

    custom_portfolio = st.data_editor(
        custom_portfolio_df,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True
    )

    custom_portfolio = custom_portfolio.dropna(how="all")

    custom_portfolio[main_pipeline.assets.index] = custom_portfolio[main_pipeline.assets.index].fillna(0)

    tmp_portfolios = []

    for id, portfolio in custom_portfolio.iterrows():
        w = np.array(portfolio[custom_portfolio.assets.index])

        if sum(w) != 0:
            w = w/sum(w)

            tmp_portfolios.append(custom_portfolio.custom_portfolio(w = w, name = portfolio['name']))

        if len(tmp_portfolios) > 0:
            custom_portfolio_list = tmp_portfolios


frontier_col, portfolio_col = st.columns([2, 1])

#with frontier_col:
plot_efficient_frontier(efficient_frontier, efficient_frontier_selected_portfolio, individual_portfolios, custom_portfolio_list, bootstrap_efficient_frontier)
#with portfolio_col:

if get_config()['active_bootstrap']:
    _, col1, col2, _ = st.columns([1,3,3,1])

    with col1:
        st.subheader(tr("subheader_selected_portfolio"))
        plot_selected_portfolio(efficient_frontier[efficient_frontier_selected_portfolio])

    with col2:
        st.subheader(tr("subheader_selected_bootstrap_portfolio"))
        plot_selected_portfolio(bootstrap_efficient_frontier[efficient_frontier_selected_portfolio])
else:
    _, col, _ = st.columns([1,2,1])

    st.subheader(tr("subheader_selected_portfolio"))
    with col:
        plot_selected_portfolio(efficient_frontier[efficient_frontier_selected_portfolio])

footer()