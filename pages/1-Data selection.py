import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from services.MarketData_V2 import MarketData_V2

from pages.utils.main_utils import *
from pages.utils.market_data_utils import *

#BASIC STREAMLIT DEFINITION

side_menu()

st.set_page_config(
    page_title="Selección de activos de modelo",
    layout='wide',
    initial_sidebar_state="collapsed"
)


first_page_load = set_page(page = 1)

#CARGA DE MARKET DATA

loaded = load_key('market_data', lambda: default_market_data())

#SI HEMOS TENIDO QUE CARGARLA, ES DECIR, SI NO ESTABA DEFINDA, RESETEAMOS EL VALOR DE LOS SELECTORES
if loaded:
    delete_key('dates_slider_selector')
    delete_key('asset_import')
    delete_key('asset_selection')

    #ELIMINAMOS EL MODELO DE COVARIANZAS YA QUE MARKET DATA HA CAMBIADO
    delete_key('returns_covariance_model')

market_data = read_key('market_data', None)

#delete_key('market_data')

if market_data is None:
    st.error(f"¡Error! Ha ocurrido un error desconocido, por favor, reinicia la aplicación.")
    st.stop()


#CARGA DE SELECTOR DE ASSETS

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
    
    #ELIMINAMOS EL MODELO DE COVARIANZAS YA QUE MARKET DATA HA CAMBIADO
    delete_key('returns_covariance_model')

#CARGA DEL IMPORTADOR DE ASSETS

if first_page_load:
    #SI REFRESCAMOS LA PAGINA POR PRIMERA VEZNO MOSTRAMOS EL ESTADO ANTERIOR, SINO LA INFORMACIÓN DE ASSETS YA IMPORTADOS

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


#AQUI, CADA VEZ QUE CAMBIAN LAS FEHCAS SE DEBERÍA ELIMINAR EL COVARIANCE Y EL PORTFOLIO MODEL, SE DEBERÍA CREAR UNA FUNCIÓN "MARKET CHANGED"

write_key('market_data', market_data)

#PLOTS

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

# ---- BOTÓN INFERIOR ----
bottom = st.container()

with bottom:
    col1, col2, col3 = st.columns([1,2,1])
    
    with col3:
        st.page_link(
            "pages/2-Covariance and returns estimation.py",
            label="Estimación de retornos y covarianzas",
            icon="🏠"
        )

# columna = market_data.returns_df.columns[0]


# st.write(market_data.total_returns_df.loc[columna])

# def extract_runs_with_variation(series, ignore_flat=True):
#     """
#     Extrae runs de crecimiento y decrecimiento
#     y calcula el porcentaje de variación de cada segmento.
    
#     Parámetros:
#     - series: pandas Series
#     - ignore_flat: si True, ignora tramos constantes
    
#     Devuelve:
#     DataFrame con información de cada run
#     """

#     series = series.reset_index(drop=True)
    
#     # 1️⃣ Diferencias y signo
#     diff = series.diff()
#     sign = np.sign(diff)

#     if ignore_flat:
#         sign = sign.replace(0, np.nan).ffill()

#     # 2️⃣ Identificar cambios de tendencia
#     run_id = (sign != sign.shift()).cumsum()

#     df = pd.DataFrame({
#         "value": series,
#         "sign": sign,
#         "run_id": run_id
#     })

#     runs = []

#     for rid, group in df.groupby("run_id"):
#         start_idx = group.index[0]
#         end_idx = group.index[-1]

#         start_value = series.iloc[start_idx]
#         end_value = series.iloc[end_idx]

#         # Evitar división por cero
#         if start_value != 0:
#             pct_change = ((end_value - start_value) / start_value) * 100
#         else:
#             pct_change = np.nan

#         runs.append({
#             "run_id": rid,
#             "type": "growth" if group["sign"].iloc[0] > 0 else "decline",
#             "start_index": start_idx,
#             "end_index": end_idx,
#             "start_value": start_value,
#             "end_value": end_value,
#             "length": len(group),
#             "pct_change": pct_change
#         })

#     return pd.DataFrame(runs)

# runs = extract_runs_with_variation(market_data.total_returns_df.loc[columna].totalReturn)

# growth_runs = runs.loc[::2]
# decline_runs = runs.loc[1::2]

# test_scatter = go.Figure()

# test_scatter.add_trace(
#     go.Scatter(
#         x=growth_runs['pct_change'],
#         y=decline_runs['pct_change'],
#         mode='markers',
#         name='Frontera eficiente'
#     )
# )

# st.plotly_chart(test_scatter, use_container_width=True)


# serie = market_data.total_returns_df.loc[columna, "totalReturn"]

# total_returns_shifted = serie.to_frame(name="totalReturn")

# total_returns_shifted["back"] = serie.shift(1)
# total_returns_shifted["front"] = serie.shift(-1)


# st.write(total_returns_shifted)

# total_returns_shifted = total_returns_shifted[
#     ((total_returns_shifted.back < total_returns_shifted.totalReturn) & (total_returns_shifted.totalReturn > total_returns_shifted.front))
#     |
#     ((total_returns_shifted.back > total_returns_shifted.totalReturn) & (total_returns_shifted.totalReturn < total_returns_shifted.front))
#     ]

# serie = market_data.total_returns_df.loc[columna, "totalReturn"]

# back = serie.shift(1)
# front = serie.shift(-1)

# local_max = (serie > back) & (serie > front)
# local_min = (serie < back) & (serie < front)

# extremos = serie[local_max | local_min]

# beats = extremos.pct_change()

# positive_beats = beats.reset_index(drop=True).iloc[::2]  
# negative_beats = beats.reset_index(drop=True).iloc[1::2]  

# st.write(beats)
# st.write(positive_beats)
# st.write(negative_beats)

# fig = go.Figure(
#     data=[
#         go.Histogram(
#             x=beats,
#             nbinsx=20  # puedes ajustar el número de bins
#         )
#     ]
# )

# fig.update_layout(
#     title="Histogram of Run Lengths",
#     xaxis_title="Run Length",
#     yaxis_title="Frequency",
# )

# st.plotly_chart(fig, use_container_width=True)

# test_scatter = go.Figure()

# test_scatter.add_trace(
#     go.Scatter(
#         x=positive_beats,
#         y=negative_beats,
#         mode='markers',
#         name = 'Frontera eficiente'
#     )
# )

# st.plotly_chart(test_scatter, use_container_width=True)

# total_returns_shifted['back'] = market_data.returns_df[columna].shift(-1)
# total_returns_shifted['front'] = market_data.returns_df[columna].shift(1)


# st.write(market_data.total_returns_df.loc[columna].totalReturn)

# groups = (df[columna] != df[columna].shift()).cumsum()

# st.write(groups)

# start_indices = df.groupby(groups).apply(lambda x: x.index[0])

# beats = market_data.total_returns_df.loc[columna].loc[start_indices]['totalReturn']

# st.write(beats)

# beats_pctchange = beats.pct_change().dropna()

# st.write(beats_pctchange)


# st.write(beats_pctchange[beats_pctchange > 0])
# st.write(beats_pctchange[beats_pctchange < 0])

# # df = market_data.returns_df>0

# # for columna in df.columns:

# #     groups = (df[columna] != df[columna].shift()).cumsum()
# #     run_lengths = df.groupby(groups).size()

# #     #st.write(run_lengths)

# #     import matplotlib.pyplot as plt

# #     values = run_lengths.tolist()

# #     values = [a + b for a, b in zip(values[::2], values[1::2])]

# #     fig = go.Figure(
# #         data=[
# #             go.Histogram(
# #                 x=values,
# #                 nbinsx=20  # puedes ajustar el número de bins
# #             )
# #         ]
# #     )

# #     fig.update_layout(
# #         title="Histogram of Run Lengths",
# #         xaxis_title="Run Length",
# #         yaxis_title="Frequency",
# #     )

# #     st.plotly_chart(fig, use_container_width=True)

# #     # st.write(values)
# #     # st.write(values[1::])

# #     transformada = [abs(v) if i % 2 == 0 else -abs(v) for i, v in enumerate(run_lengths)]


# #     test_scatter = go.Figure()

# #     test_scatter.add_trace(
# #         go.Scatter(
# #             x=market_data.returns_df[columna],
# #             y=market_data.returns_df[columna][1::],
# #             mode='markers',
# #             name = 'Frontera eficiente'
# #         )
# #     )
    
# #     st.plotly_chart(test_scatter, use_container_width=True)
