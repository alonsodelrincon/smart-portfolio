import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from services.MarketData_V2 import MarketData_V2
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

from pages.utils.main_utils import *
from pages.utils.portfolio_selection_utils import *

st.set_page_config(
    page_title="Selección del portfolio",
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 1)

#CARGA DE TODA LA CONFIGURACION

config = get_config()

# st.write(config)

#CARGA DEL ESTADO DE LOS WIDGETS

#asset_selection

#CONSTRUCCIÓN DE MARKET_DATA

load_key('market_data', lambda: default_market_data())

market_data = st.session_state.market_data

load_widget("asset_selection", list(market_data.selected_assets.index))

st.subheader("Selección de activos locales")

selected_assets = st.multiselect(
    label="Selecciona los activos del modelo",
    options= market_data.local_assets.index,
    format_func=lambda x: market_data.local_assets.loc[x].asset_name,
    key="_asset_selection",
    on_change= write_widget,
    args=["asset_selection"]
)

if set(selected_assets) != set(market_data.selected_assets.index):
    market_data.select_assets(assets=selected_assets)

    delete_key('dates_slider_selector')
    delete_key('returns_covariance_model')

if first_page_load:
    delete_key('asset_import')

load_key('asset_import', lambda: asset_import_df(market_data))

import_df = read_key('asset_import', None).reset_index(drop=True)

column_config = {
    "ticker": st.column_config.TextColumn("Ticker"),
    "asset_name": st.column_config.TextColumn("Nombre")
}

st.subheader("Importación de activos")
st.caption("Añade o edita los activos que deseas incluir en el análisis especificando su ticker y nombre (ej: AAPL - Apple).")

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
    
    #ELIMINAMOS EL MODELO DE COVARIANZAS YA QUE MARKET DATA HA CAMBIADO
    delete_key('returns_covariance_model')

#EN ESTE PUNTO VALIDAMOS EL NÚMERO DE ASSETS, SI EL ESTADO DE MARKET DATA NO ES VÁLIDO RESETEAMOS

if not market_data.valid:
    st.error(f"¡Error! Debes especificar al menos 2 activos.")

    delete_key('dates_slider_selector')

    delete_key('returns_covariance_model')

    st.stop()

load_widget(
        "dates_slider_selector", 
        (
            market_data.from_date.date(),
            market_data.to_date.date()
        )
    )

dates_slider = st.slider(
    "Selecciona el rango de fechas",
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

    delete_key('returns_covariance_model')

st.session_state.market_data = market_data

loaded = load_key('returns_covariance_model', lambda: default_covariance_model(market_data))

returns_covariance_model = st.session_state.returns_covariance_model

if loaded:
    load_covariance_model_returns(returns_covariance_model)
    load_covariance_model_covariance(returns_covariance_model)
    st.session_state.returns_covariance_model = returns_covariance_model

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
    title="Evolución del valor liquidativo de los activos",
    xaxis_title="Fecha",
    yaxis_title="Valor liquidativo",
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
    title="Rentabilidad diaria (%)",
    xaxis_title="Fecha",
    yaxis_title="Rentabilidad (%)",
    template="plotly_white"
)


st.plotly_chart(pct_returns_fig, width='stretch')

#MATRIZ DE CORRELACIÓN Y RETORNOS

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
    
    fig_cor.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig_cor.update_yaxes(tickfont=dict(size=10))
    fig_cor.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    fig_cor.update_layout(
        title="Matriz de Correlación",
        yaxis=dict(autorange="reversed"),
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
            color="#3182BD"
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

    fig_cov.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig_cov.update_yaxes(tickfont=dict(size=10))
    fig_cov.update_layout(margin=dict(l=50, r=50, t=50, b=50))

    fig_cov.update_layout(
        title="Matriz de Covarianzas diarias",
        yaxis=dict(autorange="reversed")
    )

    fig_cov.update_yaxes(
        tickfont=dict(size=10),
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_cov, width='content')


    