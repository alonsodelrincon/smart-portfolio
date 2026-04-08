import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pages.utils.main_utils import *
from pages.utils.portfolio_selection_utils import *
from pages.utils.translations import translations_portfolio_selection
from services.BasePipeline import BasePipeline
from services.BootstrapPipeline import BootstrapPipeline
import numpy as np


set_page_translations(translations_portfolio_selection, lang=get_config()['lang'])

st.set_page_config(
    page_title=tr("page_title"),
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 4)

#FUNCIONES GRÁFICAS

def plot_cor_matrix(pipeline):
    fig_cor = go.Figure(
        data=go.Heatmap(
            z=pipeline.correlation_matrix.values,
            x=[pipeline.asset_name(asset=asset) for asset in pipeline.correlation_matrix.columns],
            y=[pipeline.asset_name(asset=asset) for asset in pipeline.correlation_matrix.index],
            colorscale='Blues',
            colorbar=dict(
                len=1,
                lenmode="fraction",
                y=0.5,
                yanchor="middle"
            )
        )
    )
    
    fig_cor.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig_cor.update_yaxes(tickfont=dict(size=10))
    fig_cor.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    fig_cor.update_layout(
        title=tr("plot_correlation_matrix_title"),
        yaxis=dict(autorange="reversed"),
    )

    fig_cor.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cor, width='content')

def plot_cov_cv_matrix(bootstrap_pipeline):
    fig_cv = go.Figure(
        data=go.Heatmap(
            zmin=0,
            zmax=0.5,
            z=bootstrap_pipeline.covariance_matrix_stats['std'].values / np.abs(bootstrap_pipeline.covariance_matrix_stats['mean'].values),
            x=[bootstrap_pipeline.asset_name(asset=asset) for asset in bootstrap_pipeline.correlation_matrix.columns],
            y=[bootstrap_pipeline.asset_name(asset=asset) for asset in bootstrap_pipeline.correlation_matrix.index],
            colorscale='Blues',
            colorbar=dict(
                len=1,
                lenmode="fraction",
                y=0.5,
                yanchor="middle",
                tickformat=".0%"
            )
        )
    )
    
    fig_cv.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig_cv.update_yaxes(tickfont=dict(size=10))
    fig_cv.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    fig_cv.update_layout(
        title=tr("cov_matrix_CV"),
        yaxis=dict(autorange="reversed"),
    )

    fig_cv.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cv, width='content')

def plot_return_bars(pipeline, lower_CI = None, upper_CI = None):
    fig_expected_returns = go.Figure()

    if lower_CI is None or upper_CI is None :
        fig_expected_returns.add_trace(go.Bar(
            x=[pipeline.asset_name(asset=asset) for asset in pipeline.expected_returns.index],
            y=pipeline.expected_returns.expected_return,
            marker=dict(
                color="#3182BD"
            )
        ))
    else:
        fig_expected_returns.add_trace(go.Bar(
            x=[pipeline.asset_name(asset=asset) for asset in pipeline.expected_returns.index],
            y=pipeline.expected_returns.expected_return,
            marker=dict(
                color="#3182BD"
            ),
            
            error_y=dict(
                type='data',
                symmetric=False,
                array=upper_CI,
                arrayminus=lower_CI
            )
        ))

    fig_expected_returns.update_layout(
        title=tr("plot_expected_returns_title"),
        xaxis_title=tr("plot_expected_returns_x"),
        yaxis_title=tr("plot_expected_returns_y"),
        yaxis=dict(
            tickformat=".2%",
        ),
        template="plotly_white"
    )

    st.plotly_chart(fig_expected_returns, width='content')

def plot_return_violins(bootstrap_pipeline):
    fig = go.Figure()

    for asset in bootstrap_pipeline.bootstrap_expected_returns[0].index:
        values = [
            df.loc[asset, 'expected_return']
            for df in bootstrap_pipeline.bootstrap_expected_returns
        ]
        
        fig.add_trace(go.Violin(
            y=values,
            name=bootstrap_pipeline.asset_name(asset=asset),
            box_visible=True,
            meanline_visible=True
        ))

    fig.update_layout(
        title=tr("plot_expected_returns_title"),
        xaxis_title=tr("plot_expected_returns_x"),
        yaxis_title=tr("plot_expected_returns_y"),
        yaxis=dict(
            tickformat=".2%",
        ),
        template="plotly_white"
    )


    st.plotly_chart(fig, width='stretch')

def plot_cov_matrix(pipeline):
    fig_cov = go.Figure(
        data=go.Heatmap(
            z=pipeline.covariance_matrix.values,
            x=[pipeline.asset_name(asset=asset) for asset in pipeline.covariance_matrix.columns],
            y=[pipeline.asset_name(asset=asset) for asset in pipeline.covariance_matrix.index],
            colorscale='Blues',
            colorbar=dict(
                len=1,
                lenmode="fraction",
                y=0.5,
                yanchor="middle"
            )
        )
    )

    fig_cov.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig_cov.update_yaxes(tickfont=dict(size=10))
    fig_cov.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    fig_cov.update_layout(
        title=tr("plot_covariance_matrix_title"),
        yaxis=dict(autorange="reversed")
    )

    fig_cov.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cov, width='content')


#CONSTRUCCIÓN DE MARKET_DATA

load_key('market_data', lambda: default_market_data())

market_data = st.session_state.market_data

load_widget("asset_selection", list(market_data.selected_assets.index))

st.subheader(tr("subheader_local_assets"))

selected_assets = st.multiselect(
    label=tr("label_select_assets"),
    options= market_data.local_assets.index,
    format_func=lambda x: market_data.local_assets.loc[x].asset_name,
    key="_asset_selection",
    on_change= write_widget,
    args=["asset_selection"]
)


if set(selected_assets) != set(market_data.selected_assets.index):
    market_data.select_assets(assets=selected_assets)

    delete_key('dates_slider_selector')
    delete_key('main_pipeline')
    delete_key('bootstrap_pipeline')

if first_page_load:
    delete_key('asset_import')

load_key('asset_import', lambda: asset_import_df(market_data))

import_df = read_key('asset_import', None).reset_index(drop=True)

column_config = {
    "ticker": st.column_config.TextColumn("Ticker"),
    "asset_name": st.column_config.TextColumn("Nombre")
}

st.subheader(tr("subheader_import_assets"))
st.caption(tr("caption_import_assets"))

asset_import_data_editor = st.data_editor(
    import_df,
    column_config=column_config,
    num_rows="dynamic",
    width='content'
).dropna(how="all")


#EN EL CASO DE QUE SEA VÁLIDO Y LA INFORMACIÓN DEL DATA_EDITOR SEA DIFERENTE A LOS ASSETS IMPORTADOS DE DF, ACTUALIZAMOS LA INFORMACIÓN DE MARKET DATA
if validate_import_df(market_data, asset_import_data_editor) and not equal_imports(market_data, asset_import_data_editor):
    market_data.reset_imported_assets()

    for asset in asset_import_data_editor.itertuples():
        market_data.import_asset(ticker=asset.ticker, name=asset.asset_name, diversification=None)

    #DE IGUAL FORMA RESETEAMOS LA SELECCIÓN DE FECHAS
    delete_key('dates_slider_selector')
    
    #ELIMINAMOS EL PIPELINE YA QUE MARKET DATA HA CAMBIADO
    delete_key('main_pipeline')
    delete_key('bootstrap_pipeline')

#EN ESTE PUNTO VALIDAMOS EL NÚMERO DE ASSETS, SI EL ESTADO DE MARKET DATA NO ES VÁLIDO RESETEAMOS

if not market_data.valid:
    st.error(tr("error_min_assets"))

    delete_key('main_pipeline')
    delete_key('bootstrap_pipeline')

    st.stop()

load_widget(
        "dates_slider_selector", 
        (
            market_data.from_date.date(),
            market_data.to_date.date()
        )
    )

dates_slider = st.slider(
    tr("slider_dates"),
    min_value=market_data.first_date.date(),
    max_value=market_data.last_date.date(),
    key="_dates_slider_selector",
    on_change= write_widget,
    args=["dates_slider_selector"]
)

slider_from = pd.Timestamp(dates_slider[0])
slider_to = pd.Timestamp(dates_slider[1])

if market_data.from_date != slider_from or market_data.to_date != slider_to:
    market_data.from_date = slider_from
    market_data.to_date = slider_to

    delete_key('main_pipeline')
    delete_key('bootstrap_pipeline')

st.session_state.market_data = market_data

st.write(market_data.active_assets_metadata)

st.stop()

loaded = load_key('main_pipeline', BasePipeline(market_data=market_data))

main_pipeline = st.session_state.main_pipeline

if loaded:
    load_pipeline_returns(pipeline=main_pipeline)
    load_pipeline_covariance(pipeline=main_pipeline)

    st.session_state.pipeline = main_pipeline

if get_config()['active_bootstrap']:
    bootstrap_loaded = load_key('bootstrap_pipeline', BootstrapPipeline(
                                                        market_data=market_data, 
                                                        bootstrap_length=get_config()['bootstrap_sample_size'], 
                                                        block_length=get_config()['bootstrap_block_size']
                                                        )
                                )

    bootstrap_pipeline = st.session_state.bootstrap_pipeline

    if bootstrap_loaded:
        load_pipeline_returns(pipeline=bootstrap_pipeline)
        load_pipeline_covariance(pipeline=bootstrap_pipeline)

        st.session_state.bootstrap_pipeline = bootstrap_pipeline

#---------------------------------------------------
#-----------------------PLOTS-----------------------
#---------------------------------------------------


#RETORNOS TOTALES

total_returns_fig = go.Figure()

assets = market_data.returns_df.columns
names = market_data.active_assets

for asset in assets:
    data = market_data.total_returns_df.loc[asset]
    total_returns_fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data.totalReturn,
            mode='lines',
            name = market_data.asset_name(asset=asset)
        )
    )

total_returns_fig.update_layout(
    title=tr("plot_total_returns_title"),
    xaxis_title=tr("plot_total_returns_x"),
    yaxis_title=tr("plot_total_returns_y"),
    template="plotly_white"
)

st.plotly_chart(total_returns_fig, width='stretch')

#VARIACIÓN PORCENTUAL DIARIA

pct_returns_fig = go.Figure()

assets = market_data.returns_df.columns
names = market_data.active_assets

for asset in assets:
    pct_returns_fig.add_trace(
        go.Scatter(
            x=market_data.returns_df.index,
            y=market_data.returns_df[asset],
            mode='lines',
            name = market_data.asset_name(asset=asset)
        )
    )

pct_returns_fig.update_layout(
    title=tr("plot_pct_returns_title"),
    xaxis_title=tr("plot_pct_returns_x"),
    yaxis_title=tr("plot_pct_returns_y"),
    template="plotly_white"
)


st.plotly_chart(pct_returns_fig, width='stretch')


st.subheader(tr("simple_estimates"))

#MATRIZ DE CORRELACIÓN Y RETORNOS

cor, returns = st.columns([1, 1])

with cor:
    plot_cor_matrix(main_pipeline)
    
with returns:
    plot_return_bars(main_pipeline)

#MATRIZ DE COVARIANZA

with st.expander(tr("expander_covariance_matrix")):
    plot_cov_matrix(main_pipeline)

if get_config()['active_bootstrap']:
    st.subheader(tr("bootstrap_estimates"))

    plot_return_violins(bootstrap_pipeline)

    #MATRIZ DE CORRELACIÓN Y RETORNOS (BOOTSTRAP)

    cov, cov_CV = st.columns([1, 1])

    with cov:
        plot_cov_matrix(bootstrap_pipeline)

    with cov_CV:
        plot_cov_cv_matrix(bootstrap_pipeline)

footer()