import streamlit as st
from pages.utils.main_utils import *
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import make_interp_spline
from pages.utils.translations import translations_app

set_page_translations(translations_app, lang=get_config()['lang'])

st.set_page_config(
    page_title="Inicio",
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 0)

st.header(tr("welcome"))

# Sobre el proyecto
st.subheader(tr("about_project"))
st.markdown(tr("about_project_text"))


# Principales aspectos
st.subheader(tr("main_points"))
st.markdown(tr("main_points_text"))

# Cómo utilizar la app
st.subheader(tr("how_to_use"))

st.markdown(f"### {tr('select_assets')}")
st.markdown(tr("select_assets_text"))

st.markdown(f"### {tr('efficient_frontier')}")
st.markdown(tr("efficient_frontier_text"))

st.markdown(f"### {tr('config')}")
st.markdown(tr("config_text"))

# Modelo de frontera eficiente
st.subheader(tr("efficient_model"))
st.markdown(tr("efficient_model_text"))

portfolio_risks = [0.1826193372483225,0.18542816014731894,0.18819501229657787,0.19092185926910815,0.19361020032383336,0.19626173871483563,0.1988779987613756,0.20146028004134023,0.20400982947743487,0.206527792781088,0.20901580758875551]
portfolio_returns = [0.16194573926416922,0.16522076997580526,0.16658862546197262,0.16763934265997604,0.1685258378804737,0.1693074192281241,0.17001449040836203,0.17066508349688592,0.1712709529986145,0.17184025755704968,0.17237905561751599]

efficient_frontier_fig = go.Figure()

# Supongamos que portfolio_risks y portfolio_returns son arrays de numpy
x = np.array(portfolio_risks)
y = np.array(portfolio_returns)

# Crear un nuevo eje x más denso para suavizar la curva
x_smooth = np.linspace(x.min(), x.max(), 100)  # 500 puntos para suavizar

# Interpolación cúbica
spl = make_interp_spline(x, y, k=3)  # k=3 → cúbica
y_smooth = spl(x_smooth)

# Añadir a Plotly
efficient_frontier_fig.add_trace(
    go.Scatter(
        x=x_smooth,
        y=y_smooth,
        mode='lines',
        name=tr("efficient_frontier_plot")
    )
)

efficient_frontier_fig.update_layout(
    title="",
    xaxis=dict(
        title = tr("risk"),
        #range=[min(portfolio_risks), max(portfolio_risks)],
        #fixedrange=False  # True si quieres que no se pueda hacer zoom
    ),
    yaxis=dict(
        title = tr("return"),
        #range=[min(portfolio_returns), max(portfolio_returns)],
        #fixedrange=False  # True si quieres que no se pueda hacer zoom
    ),
    template="plotly_white"
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[portfolio_risks[0]],
        y=[portfolio_returns[0]],
        mode='markers',
        marker=dict(size=10, color='lightblue'),
        name = tr("min_variance"),
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[portfolio_risks[len(portfolio_risks)-1]],
        y=[portfolio_returns[len(portfolio_returns)-1]],
        mode='markers',
        marker=dict(size=10, color='darkblue'),
        name = tr("max_return"),
    )
)

# Punto 1: Cartera genérica
x_gen, y_gen = 0.19626173871483563, 0.16522076997580526
# Punto 2: Igual rentabilidad y mínimo riesgo
x_minrisk, y_minrisk = 0.18542816014731894, 0.16522076997580526
# Punto 3: Igual riesgo y máxima rentabilidad
x_maxret, y_maxret = 0.19626173871483563, 0.1693074192281241

# Línea horizontal: misma rentabilidad
efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_gen, x_minrisk],
        y=[y_gen, y_minrisk],
        mode='lines',
        line=dict(color='red', dash='dash'),
        showlegend=False
    )
)

# Línea vertical: mismo riesgo
efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_gen, x_maxret],
        y=[y_gen, y_maxret],
        mode='lines',
        line=dict(color='red', dash='dash'),
        showlegend=False
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_minrisk],
        y=[y_gen],
        mode='markers',
        marker=dict(size=10, color="darkred"),
        name = tr("equal_return_min_risk"),
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_gen],
        y=[y_maxret],
        mode='markers',
        marker=dict(size=10, color='red'),
        name = tr("equal_risk_max_return"),
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_gen],
        y=[y_gen],
        mode='markers',
        marker=dict(size=10, color='green'),
        name = tr("non_optimal"),
    )
)

st.plotly_chart(efficient_frontier_fig, width="stretch")

# Explicación de la gráfica
st.markdown(tr("chart_explanation"))

# Más detalles
st.markdown(f"### {tr('more_details')}")
st.markdown(tr("more_details_text"))

footer()