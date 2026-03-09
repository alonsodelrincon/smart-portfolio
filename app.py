import streamlit as st
from pages.utils.main_utils import *
from services.ReturnsCovarianceModel import ReturnsCovarianceModel
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import make_interp_spline

st.set_page_config(
    page_title="Inicio",
    layout='wide',
    #initial_sidebar_state="collapsed"
)

side_menu()

first_page_load = set_page(page = 0)

# st.header("Bienvenid@ a SmartPortfolio")

# st.markdown("""
# ## Sobre el proyecto

# Smart portfolio es una app dedicada al análsis de activos financieros bajo el prisma del modelo de la cartera eficiente. Su principal objetivo es calcular qué combinaciones de activos ofercen una rentabilidad óptima de rentabilidad/riesgo. 
# Esta aplicación está construida de una manera amigable tal que le permita a usuarios no expertos en la matera analizar con rigor diferentes carteras para tomar mejores decisiones financieras.

# ## Principales aspectos
            
# - Selección e importación: selecciona e importa diferentes activos para realizar el análisis. 
# - Frontera eficiente: Navega sobre la frontera eficiente calculada sobre los activos seleccionados y compárala con carteras personalizadas para evaluar su relacción rentabilidad/riesgo.
# - Configuración extensa: Especifica los métodos y parámetros usados en los procesos de estimación de la rentabilidad esperarda y la matriz de covarianzas.

# ### Cómo utilizarlo
            
# - 💹 Selección de activos:
#     - Selección de activos locales: especifica los activos que deseas icorporar a tu análisis de entre una amplia lista ya precargada.
#     - Importación de activos: importa otros activos facilitando su ticker.
#     - Selecciónd de fechas: especifica qué rango temporal deseas estudiar.
#     - Martices de correlación y retornos esperados: podrás ver de una manera sencilla que correlaciones existen entre tus activos así como cual es la rentabilidad esperada de cada uno de ellos.

# - 📊 Análisis de la frontera eficiente:
#     - Para los activos seleccionados, podrás ver su frontera eficiente asociada y navegar sobre ella con un selector descubriendo las combinaciones de activos óptimas.
#     - Podrás especificar cotras carteras personalizadas para poder evaluarlas en contraste con la frontera eficiente.
            
# - ⚙️ Configuración:
#     - Especifica la base de datos conde se encuentran los activos locales disponibles.
#     - Especifica los diferentes aspectos relaccionados con el cálculo de la rentabilidad estimada (método de estimación, bandwidth ...)
#     - Especifica los diferentes aspectos relaccionados con el cálculo de la matriz de covarianzas (método de estimación, bandwidth, kernel ...)
# """)

st.header("Bienvenid@ a SmartPortfolio")

st.subheader("📖 Sobre el proyecto")

st.markdown("""
**SmartPortfolio** es una aplicación dedicada al análisis de activos financieros bajo el prisma del **modelo de la cartera eficiente**.

Su principal objetivo es calcular qué combinaciones de activos ofrecen una relación óptima **rentabilidad/riesgo**.

La aplicación está diseñada de forma intuitiva para que usuarios no expertos puedan analizar diferentes carteras con rigor y tomar mejores decisiones financieras.
""")

st.subheader("⭐ Principales aspectos")

st.markdown("""
- **Selección e importación de activos**  
  Permite seleccionar activos de una base de datos local o importar nuevos activos mediante su ticker.

- **Frontera eficiente**  
  Navega sobre la frontera eficiente calculada para los activos seleccionados y compárala con carteras personalizadas.

- **Configuración avanzada**  
  Permite seleccionar diferentes parámetros y métodos usados en la estimación de rentabilidad esperada y matriz de covarianzas.
""")

st.subheader("🧭 Cómo utilizar la aplicación")

st.markdown("### 💹 Selección de activos")

st.markdown("""
- **Selección de activos locales**  
  Especifica los activos que deseas incorporar a tu análisis de entre una lista ya precargada.

- **Importación de activos**  
  Permite importar nuevos activos introduciendo su ticker.

- **Selección de fechas**  
  Define el rango temporal que deseas estudiar.

- **Matrices de correlación y retornos esperados**  
  Visualiza de forma sencilla las correlaciones entre activos y la rentabilidad esperada de cada uno.
""")

st.markdown("### 📊 Análisis de la frontera eficiente")

st.markdown("""
- **Visualización de la frontera eficiente**  
  Para los activos seleccionados podrás visualizar la frontera eficiente asociada.

- **Exploración interactiva**  
  Navega sobre la frontera usando un selector para descubrir las combinaciones óptimas de activos.

- **Comparación con carteras personalizadas**  
  Define carteras propias y compáralas con la frontera eficiente para evaluar su relación **rentabilidad/riesgo**.
""")

st.markdown("### ⚙️ Configuración")

st.markdown("""
- **Base de datos de activos**  
  Especifica la base de datos donde se encuentran los activos locales disponibles.

- **Estimación de rentabilidad esperada**  
  Configura el método de estimación y parámetros como el *bandwidth*.

- **Estimación de la matriz de covarianzas**  
  Define el método de estimación, kernel y otros parámetros utilizados en el cálculo.
""")

st.subheader("🛠️ ¿Cómo funciona el modelo de la frontera eficiente?")

# st.markdown("""
# La frontera eficiente parte del cálculo de la matriz de covarianzas asociada a nuestros activos $\Sigma$ así como de el vector de rentabilidad esperada $\mu$.
            
# Para una lista de $n$ activos disponibles $(a_1, a_2, \dots, a_n)$ podremos definir una cartera concreta a través de los pesos que cada activo tiene en esta. Más formalmente, cada cartera será representdada por un vector de probabilidad es decir:
            
# $$
# (w_1, w_2, \dots, w_n) \in [0,1]^n \quad \text{con} \quad \sum_{i=1}^{n} w_i = 1
# $$

# donde:

# - $w_i$ es el peso del activo $i$ en la cartera
# - La suma de todos los pesos es 1
# - Cada peso está entre 0 y 1

# """)

st.markdown(r"""
La frontera eficiente parte del cálculo de la matriz de covarianzas asociada a nuestros activos $\Sigma$ así como del vector de rentabilidad esperada $\mu$.
            
Para una lista de $n$ activos disponibles $(a_1, a_2, \dots, a_n)$ una cartera queda definida por la proporción de que cada activo en esta. Más formalmente, cada cartera será representdada por un vector de probabilidad:
    
$$
\mathbf{w} = (w_1, w_2, \dots, w_n) \in [0,1]^n \quad \text{con} \quad \sum_{i=1}^{n} w_i = 1
$$
            
Es decir:

- $w_i$ es el peso del activo $i$ en la cartera.
- La suma de todos los pesos es 1.
- Cada peso está entre 0 y 1 (no consideramos ventas en corto).
            
Para cualquier cartera con un vector de pesos asociado $\mathbf{w}$ podemos calcular su varianza $\hat{\sigma}^2$ y rentabilidad esperada $\hat{\mu}$ de la siguiente forma:
            
$$

\hat{\sigma}^2 = \mathbf{w} \Sigma \mathbf{w}^\top = 
\begin{pmatrix} w_1 & w_2 & \dots & w_n \end{pmatrix}
\begin{pmatrix}
\sigma_{11} & \sigma_{12} & \dots & \sigma_{1n} \\
\sigma_{21} & \sigma_{22} & \dots & \sigma_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
\sigma_{n1} & \sigma_{n2} & \dots & \sigma_{nn}
\end{pmatrix}
\begin{pmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{pmatrix}

$$
            
$$
\hat{\mu} = \mu \mathbf{w}^\top =
    \begin{pmatrix} \mu_1 & \mu_2 & \dots & \mu_n \end{pmatrix} \begin{pmatrix} w_1 \\ w_2 \\ \dots \\ w_n \end{pmatrix}     
$$

            
El modelo de la frontera eficiente busca calcular para cada rentabilidad esperada $\mu_p$, la cartera $\mathbf{w}$ que proporcione la mínima varianza factible $\sigma_p$. Más 
concretamente, definimos como frontera eficiente al conjunto de pares que cumplen esta propiedad:
            
$$
    \{ (\mu_p, \sigma_p) |  \sigma_p= \min_{\mathbf{w}} \sqrt{\mathbf{w} \Sigma \mathbf{w}^\top} \quad \text{sujeto a} \quad \mu \mathbf{w}^\top = \mu_p  \}
$$
            
A continuación, podemos observar un ejemplo de frontera eficiente:
""")

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
        name='Frontera eficiente'
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

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[portfolio_risks[0]],
        y=[portfolio_returns[0]],
        mode='markers',
        marker=dict(size=10, color='lightblue'),
        name = 'Cartera de mínima varianza',
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[portfolio_risks[len(portfolio_risks)-1]],
        y=[portfolio_returns[len(portfolio_returns)-1]],
        mode='markers',
        marker=dict(size=10, color='darkblue'),
        name = 'Cartera de máxima rentabilidad',
    )
)

# Punto 1: Cartera genérica
x_gen, y_gen = 0.19626173871483563, 0.16522076997580526
# Punto 2: Igual rentabilidad y mínimo riesgo
x_minrisk, y_minrisk = 0.18542816014731894, 0.16522076997580526
# Punto 3: Igual riesgo y máxima rentabilidad
x_maxret, y_maxret = 0.19626173871483563, 0.1693074192281241

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_minrisk],
        y=[y_gen],
        mode='markers',
        marker=dict(size=10, color='red'),
        name = 'Cartera de igual rentabilidad y mínimo riesgo',
    )
)

efficient_frontier_fig.add_trace(
    go.Scatter(
        x=[x_gen],
        y=[y_maxret],
        mode='markers',
        marker=dict(size=10, color='red'),
        name = 'Cartera de igual riesgo y máxima rentabilidad',
    )
)

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
        x=[x_gen],
        y=[y_gen],
        mode='markers',
        marker=dict(size=10, color='green'),
        name = 'Cartera no óptima',
    )
)

st.plotly_chart(efficient_frontier_fig, width="stretch")

st.markdown("""
Como hemos visto, cada punto de la frontera representa una combinación **rentabilidad/riesgo** óptima. Como se puede ver, si una cartera no esta sobre la frontera, es decir, 
no es óptima, siempre podremos encontrar otra cartera que nos ofezca más rentabilidad por el mismo riesgo asumido o la misma rentabilidad para un menor riesgo.
            
Hay dos carteras a destacar en la frontera eficiente. Estas son:

- **Cartera de mínima varianza**  
  Es la cartera que menor riesgo ofrece.

- **Cartera de máxima rentabilidad**  
  Es la cartera que máx rentabilidad ofrece. Siempre corresponde con la cartera compuesta en un 100% del activo de más rentabilidad.
""")

footer()