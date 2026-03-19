translations_app = {
    "es": {
        "welcome": "Bienvenid@ a SmartPortfolio",
        "about_project": "📖 Sobre el proyecto",
        "about_project_text": (
            "**SmartPortfolio** es una aplicación dedicada al análisis de activos financieros "
            "bajo el prisma del **modelo de la cartera eficiente**.\n\n"
            "Su principal objetivo es calcular qué combinaciones de activos ofrecen una relación óptima **rentabilidad/riesgo**.\n\n"
            "La aplicación está diseñada de forma intuitiva para que usuarios no expertos puedan analizar diferentes carteras con rigor y tomar mejores decisiones financieras."
        ),
        "main_points": "⭐ Principales aspectos",
        "main_points_text": (
            "- **Selección e importación de activos**  \n"
            "  Permite seleccionar activos de una base de datos local o importar nuevos activos mediante su ticker.\n\n"
            "- **Frontera eficiente**  \n"
            "  Navega sobre la frontera eficiente calculada para los activos seleccionados y compárala con carteras personalizadas.\n\n"
            "- **Configuración avanzada**  \n"
            "  Permite seleccionar diferentes parámetros y métodos usados en la estimación de rentabilidad esperada y matriz de covarianzas."
        ),
        "how_to_use": "🧭 Cómo utilizar la aplicación",
        "select_assets": "💹 Selección de activos",
        "select_assets_text": (
            "- **Selección de activos locales**  \n"
            "  Especifica los activos que deseas incorporar a tu análisis de entre una lista ya precargada.\n\n"
            "- **Importación de activos**  \n"
            "  Permite importar nuevos activos introduciendo su ticker.\n\n"
            "- **Selección de fechas**  \n"
            "  Define el rango temporal que deseas estudiar.\n\n"
            "- **Matrices de correlación y retornos esperados**  \n"
            "  Visualiza de forma sencilla las correlaciones entre activos y la rentabilidad esperada de cada uno."
        ),
        "efficient_frontier": "📊 Análisis de la frontera eficiente",
        "efficient_frontier_text": (
            "- **Visualización de la frontera eficiente**  \n"
            "  Para los activos seleccionados podrás visualizar la frontera eficiente asociada.\n\n"
            "- **Exploración interactiva**  \n"
            "  Navega sobre la frontera usando un selector para descubrir las combinaciones óptimas de activos.\n\n"
            "- **Comparación con carteras personalizadas**  \n"
            "  Define carteras propias y compáralas con la frontera eficiente para evaluar su relación **rentabilidad/riesgo**."
        ),
        "config": "⚙️ Configuración",
        "config_text": (
            "- **Base de datos de activos**  \n"
            "  Especifica la base de datos donde se encuentran los activos locales disponibles.\n\n"
            "- **Estimación de rentabilidad esperada**  \n"
            "  Configura el método de estimación y parámetros como el *bandwidth*.\n\n"
            "- **Estimación de la matriz de covarianzas**  \n"
            "  Define el método de estimación, kernel y otros parámetros utilizados en el cálculo."
        ),
        "efficient_model": "🛠️ ¿Cómo funciona el modelo de la frontera eficiente?",
        "efficient_model_text": r"""
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
        """,
        "chart_explanation": (
            "Como hemos visto, cada punto de la frontera representa una combinación **rentabilidad/riesgo** óptima. "
            "Si una cartera no está sobre la frontera, es decir, no es óptima, siempre podremos encontrar otra cartera que nos ofrezca más rentabilidad por el mismo riesgo asumido o la misma rentabilidad para un menor riesgo.\n\n"
            "Hay dos carteras a destacar en la frontera eficiente:\n\n"
            "- **Cartera de mínima varianza**  \n"
            "  Es la cartera que menor riesgo ofrece.\n\n"
            "- **Cartera de máxima rentabilidad**  \n"
            "  Es la cartera que máxima rentabilidad ofrece. Siempre corresponde con la cartera compuesta en un 100% del activo de más rentabilidad."
        ),
        "more_details": "🔗 Más detalles del proyecto",
        "more_details_text": (
            "Si quieres ver más información o código del proyecto completo, "
            "entra en el siguiente repositorio de GitHub: "
            "[Proyecto Completo](https://github.com/alonsodelrincon/smart-portfolio)"
        ),
        "risk": "Riesgo anual",
        "return": "Rentabilidad (%)",
        "efficient_frontier_plot": "Frontera eficiente",
        "min_variance": "Cartera de mínima varianza",
        "max_return": "Cartera de máxima rentabilidad",
        "equal_return_min_risk": "Cartera de igual rentabilidad y mínimo riesgo",
        "equal_risk_max_return": "Cartera de igual riesgo y máxima rentabilidad",
        "non_optimal": "Cartera no óptima"
    },
    "en": {
        "welcome": "Welcome to SmartPortfolio",
        "about_project": "📖 About the project",
        "about_project_text": (
            "**SmartPortfolio** is an application dedicated to analyzing financial assets "
            "through the lens of the **efficient frontier model**.\n\n"
            "Its main goal is to calculate which asset combinations provide an optimal **return/risk** ratio.\n\n"
            "The app is designed intuitively so that non-expert users can rigorously analyze different portfolios and make better financial decisions."
        ),
        "main_points": "⭐ Main points",
        "main_points_text": (
            "- **Asset selection and import**  \n"
            "  Allows selecting assets from a local database or importing new assets via their ticker.\n\n"
            "- **Efficient frontier**  \n"
            "  Explore the efficient frontier for selected assets and compare it with custom portfolios.\n\n"
            "- **Advanced configuration**  \n"
            "  Allows selecting different parameters and methods for estimating expected returns and covariance matrix."
        ),
        "how_to_use": "🧭 How to use the app",
        "select_assets": "💹 Asset selection",
        "select_assets_text": (
            "- **Select local assets**  \n"
            "  Choose assets from a preloaded list.\n\n"
            "- **Import assets**  \n"
            "  Add new assets by entering their ticker.\n\n"
            "- **Select dates**  \n"
            "  Define the time range to analyze.\n\n"
            "- **Correlation and expected returns matrices**  \n"
            "  Easily visualize correlations between assets and their expected returns."
        ),
        "efficient_frontier": "📊 Efficient frontier analysis",
        "efficient_frontier_text": (
            "- **Visualize the efficient frontier**  \n"
            "  See the efficient frontier for the selected assets.\n\n"
            "- **Interactive exploration**  \n"
            "  Use a slider to explore optimal asset combinations.\n\n"
            "- **Compare with custom portfolios**  \n"
            "  Define your own portfolios and compare them with the efficient frontier."
        ),
        "config": "⚙️ Configuration",
        "config_text": (
            "- **Assets database**  \n"
            "  Specify the database where local assets are stored.\n\n"
            "- **Expected return estimation**  \n"
            "  Set the estimation method and parameters like bandwidth.\n\n"
            "- **Covariance matrix estimation**  \n"
            "  Define the estimation method, kernel, and other parameters used in the calculation."
        ),
        "efficient_model": "🛠️ How the efficient frontier model works",
        "efficient_model_text": r"""
        The efficient frontier starts from the calculation of the covariance matrix associated with our assets $\Sigma$ as well as the expected returns vector $\mu$.
                    
        For a list of $n$ available assets $(a_1, a_2, \dots, a_n)$, a portfolio is defined by the proportion of each asset in it. Formally, each portfolio is represented by a probability vector:
            
        $$
        \mathbf{w} = (w_1, w_2, \dots, w_n) \in [0,1]^n \quad \text{with} \quad \sum_{i=1}^{n} w_i = 1
        $$
                    
        That is:

        - $w_i$ is the weight of asset $i$ in the portfolio.
        - The sum of all weights is 1.
        - Each weight is between 0 and 1 (short selling is not considered).
                    
        For any portfolio with an associated weight vector $\mathbf{w}$, we can calculate its variance $\hat{\sigma}^2$ and expected return $\hat{\mu}$ as follows:
                    
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

                    
        The efficient frontier model aims to calculate, for each expected return $\mu_p$, the portfolio $\mathbf{w}$ that provides the minimum feasible variance $\sigma_p$. More specifically, the efficient frontier is defined as the set of pairs that satisfy this property:
                    
        $$
            \{ (\mu_p, \sigma_p) |  \sigma_p= \min_{\mathbf{w}} \sqrt{\mathbf{w} \Sigma \mathbf{w}^\top} \quad \text{subject to} \quad \mu \mathbf{w}^\top = \mu_p  \}
        $$
                    
        Below, we can see an example of the efficient frontier:
        """,
        "chart_explanation": (
            "As we can see, each point on the frontier represents an optimal **return/risk** combination. "
            "If a portfolio is not on the frontier, it is non-optimal, and we can always find another portfolio that offers more return for the same risk or the same return for less risk.\n\n"
            "Two portfolios stand out on the efficient frontier:\n\n"
            "- **Minimum variance portfolio**  \n"
            "  The portfolio with the lowest risk.\n\n"
            "- **Maximum return portfolio**  \n"
            "  The portfolio with the highest return. It usually consists 100% of the highest-return asset."
        ),
        "more_details": "🔗 More project details",
        "more_details_text": (
            "For more information or the full code, visit the GitHub repository: "
            "[Full Project](https://github.com/alonsodelrincon/smart-portfolio)"
        ),
        "risk": "Annual risk",
        "return": "Return (%)",
        "efficient_frontier_plot": "Efficient frontier",
        "min_variance": "Minimum variance portfolio",
        "max_return": "Maximum return portfolio",
        "equal_return_min_risk": "Portfolio with equal return and minimum risk",
        "equal_risk_max_return": "Portfolio with equal risk and maximum return",
        "non_optimal": "Non-optimal portfolio"
    }
}

translations_portfolio_selection = {
    "es": {
        "page_title": "Selección del portfolio",
        "subheader_local_assets": "Selección de activos locales",
        "label_select_assets": "Selecciona los activos del modelo",
        "subheader_import_assets": "Importación de activos",
        "caption_import_assets": (
            "Añade o edita los activos que deseas incluir en el análisis "
            "especificando su ticker y nombre (ej: AAPL - Apple)."
        ),
        "error_min_assets": "¡Error! Debes especificar al menos 2 activos.",
        "slider_dates": "Selecciona el rango de fechas",
        "plot_total_returns_title": "Evolución del valor liquidativo de los activos",
        "plot_total_returns_x": "Fecha",
        "plot_total_returns_y": "Valor liquidativo",
        "plot_pct_returns_title": "Rentabilidad diaria (%)",
        "plot_pct_returns_x": "Fecha",
        "plot_pct_returns_y": "Rentabilidad (%)",
        "plot_correlation_matrix_title": "Matriz de Correlación",
        "plot_expected_returns_title": "Rentabilidad diaria estimada (%)",
        "plot_expected_returns_x": "Activos",
        "plot_expected_returns_y": "Rentabilidad (%)",
        "expander_covariance_matrix": "Matriz de covarianzas",
        "plot_covariance_matrix_title": "Matriz de Covarianzas diarias"
    },
    "en": {
        "page_title": "Portfolio Selection",
        "subheader_local_assets": "Local asset selection",
        "label_select_assets": "Select model assets",
        "subheader_import_assets": "Asset import",
        "caption_import_assets": (
            "Add or edit the assets you want to include in the analysis "
            "by specifying their ticker and name (e.g., AAPL - Apple)."
        ),
        "error_min_assets": "Error! You must specify at least 2 assets.",
        "slider_dates": "Select the date range",
        "plot_total_returns_title": "Net asset value evolution",
        "plot_total_returns_x": "Date",
        "plot_total_returns_y": "Net value",
        "plot_pct_returns_title": "Daily return (%)",
        "plot_pct_returns_x": "Date",
        "plot_pct_returns_y": "Return (%)",
        "plot_correlation_matrix_title": "Correlation matrix",
        "plot_expected_returns_title": "Estimated daily return (%)",
        "plot_expected_returns_x": "Assets",
        "plot_expected_returns_y": "Return (%)",
        "expander_covariance_matrix": "Covariance matrix",
        "plot_covariance_matrix_title": "Daily covariance matrix"
    }
}

translations_config = {
    "es": {
        "page_title": "Configuración",
        "header_language": "Idioma",
        "language_selector_label": "Selecciona tu idioma",
        "language_apply": "Aplicar",
        "header_database": "Configuración de la base de datos",
        "db_description": "La base de datos contendrá los activos locales que se podrán seleccionar para ejecutar el análisis.",
        "db_selector_label": "Especifica la fuente de datos a usar",
        "header_expected_return": "Configuración de los métodos de estimación",
        "subheader_expected_return": "Rentabilidad esperada",
        "select_method_expected_return": "Método de estimación",
        "select_bandwidth_method": "Método de cálculo de número de observaciones utilizadas (bandwidth)",
        "input_bandwidth_value": "Define el bandwidth",
        "slider_lambda": "Selecciona $$\\lambda$$",
        "expander_simple": "Método de estimación de rentabilidad: **Simple**",
        "expander_simple_text": r"""
        Este método define la rentabilidad esperada del activo $i$ como
        $$
        \hat{\mu}_i = \frac{1}{T} \sum_{t=0}^{T} R_{i,t}.
        $$
        """,
        "expander_ewma": "Método de estimación de rentabilidad: **Exponential Moving Average**",
        "expander_ewma_text": r"""
        Este método define la rentabilidad del activo $i$ como
        $$
        \hat{\mu}_i = (1-\lambda) \sum_{t=0}^{T} \lambda^{T-t} R_{i,t}.
        $$
        """,
        "expander_barlett": "Método de estimación de rentabilidad: **Barlett Kernel**",
        "expander_barlett_text": r"""
        Este método define la rentabilidad del activo $i$ como
        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Donde $w_t$ es el kernel de Barlett definido como

        $$
        w_t = \frac{t}{T}.
        $$
        """,
        "expander_parzen": "Método de estimación de rentabilidad: **Parzen Kernel**",
        "expander_parzen_text": r"""
        Este método define la rentabilidad del activo $i$ como
        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Donde $w_t$ es el kernel de Parzen definido como:

        $$
        w_t =
        \begin{cases}
        1 - 6 \left( \frac{t}{T} \right)^{2} + 6 \left( \frac{t}{T} \right)^{3}, & \text{si } t \le \lfloor \frac{T}{2} \rfloor \\[2mm]
        2 \left( 1 - \frac{t}{T} \right)^{3}, & \text{si } t > \lfloor \frac{T}{2} \rfloor
        \end{cases}.
        $$
        """,
        "expander_tuckey": "Método de estimación de rentabilidad: **Tuckey Hanning**",
        "expander_tuckey_text": r"""
        Este método define la rentabilidad del activo $i$ como

        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Donde $w_t$ es el kernel de Tukey-Hanning definido como:

        $$
        w_t = \frac{1}{2} \left( 1 + \cos\left( \frac{\pi t}{T} \right) \right)
        $$
        """,
        "expander_trim": "Método de estimación de rentabilidad: **Media recortada**",
        "expander_trim_text": r"""
        La media recortada estima la rentabilidad esperada del activo $i$
        como la media de las rentabilidades diarias excluyendo los percentiles extremos (por ejemplo 5% y 95%):

        $$
        \hat{\mu}_i = \frac{1}{|S_i|} \sum_{t \in S_i} R_{i,t}, \quad
        S_i = \{ t : R_{i,t} \in [P_{5\%}, P_{95\%}] \}
        $$
        """,
        "expander_wins": "Método de estimación de rentabilidad: **Media winsorizada**",
        "expander_wins_text": r"""
        La media winsorizada define la rentabilidad esperada del activo $i$
        reemplazando los extremos por los percentiles antes de calcular la media:

        $$
        \hat{\mu}_i = \frac{1}{T} \sum_{t=0}^{T} \tilde{R}_{i,t}, \quad
        \tilde{R}_{i,t} =
        \begin{cases}
        P_{5\%}, & \text{si } R_{i,t} < P_{5\%} \\
        R_{i,t}, & \text{si } P_{5\%} \le R_{i,t} \le P_{95\%} \\
        P_{95\%}, & \text{si } R_{i,t} > P_{95\%}
        \end{cases}
        $$
        """,
        "expander_shrinkage": "Método de estimación de rentabilidad: **Estimador de media con shrinkage**",
        "expander_shrinkage_text": r"""
        Con shrinkage, la rentabilidad esperada se calcula combinando la media histórica de cada activo
        con la media global de todos los activos, ponderados por un factor $\lambda$:

        $$
        \hat{\mu}_i^{\text{shrink}} = \lambda \hat{\mu}_i^{\text{hist}} + (1-\lambda) \bar{\mu}
        $$

        Donde:

        - $\hat{\mu}_i^{\text{hist}}$ es la media histórica de las rentabilidades del activo $i$  
        - $\bar{\mu}$ es la media de la rentabilidad de todos los activos  
        - $\lambda \in [0,1]$ es el factor de shrinkage
        """,
        "expander_newey_west_bandwidth": "Selección del número óptimo de observaciones: **Newey–West**",
        "expander_newey_west_bandwidth_text": r"""
        El bandwidth se calcula como:

        $$
        B = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
        $$

        donde $T$ es el número total de retornos de nuestra serie.
        """,
        "expander_andrews_plugin_bandwidth": "Selección del número óptimo de observaciones: **Regla de Andrews**",
        "expander_andrews_plugin_bandwidth_text": r"""
        El bandwidth se calcula como:

        $$
        B = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
        $$

        donde $T$ es el número total de retornos de nuestra serie.
        """,
        "subheader_covariance_matrix": "Matriz de covarianzas",
        "select_method_covariance": "Método de estimación",
        "select_cov_bandwidth_method": "Método de cálculo de retardos",
        "input_cov_bandwidth_value": "Número de retardos (L)",
        "expander_cov_simple": "Método de estimación de la covarianza: **Simple**",
        "expander_cov_simple_text": r"""
        Este método considera la matriz de covarianzas $$\Sigma$$ tal que

        $$
        \Sigma_{i,j} = Cov(R_i, R_j).
        $$
        """,
        "expander_cov_newey": "Método de estimación de la covarianza: **Newey-West**",
        "expander_cov_newey_text": r"""
        Este método estima la matriz de covarianzas teniendo en cuenta 
        autocorrelación hasta un cierto número de retardos $$L$$.

        $$
        \Sigma = \sum_{t=0}^{L} w_t \, \Sigma_t.
        $$

        Donde $w_t$ es el kernel de Barlett:

        $$
        w_t = \frac{L - t}{L}
        $$

        y $$\Sigma_{t}$$ es la matriz de covarianzas entre los retornos actuales 
        y los retornos desplazados $$t$$ periodos.
        """,
        "expander_newey_west_lags": "Selección del número óptimo de retardos: **Newey–West**",
        "expander_newey_west_lags_text": r"""
        El número de retardos usados se calcula como:

        $$
        L = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
        $$

        donde $T$ es el número total de retornos de nuestra serie.
        """,
        "expander_andrews_plugin_lags": "Selección del número óptimo de retardos: **Regla de Andrews**",
        "expander_andrews_plugin_lags_text": r"""
        El número de retardos usados se calcula como:

        $$
        L = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
        $$

        donde $T$ es el número total de retornos de nuestra serie.
        """,
        "header_efficient_frontier": "Configuración del tamaño de la frontera eficiente",
        "input_efficient_n_steps": "Número de carteras a calcular en la frontera eficiente"
    },
    "en": {
        "page_title": "Settings",
        "header_language": "Language",
        "language_selector_label": "Select your language",
        "language_apply": "Apply",
        "header_database": "Database Configuration",
        "db_description": "The database will contain the local assets that can be selected for analysis execution.",
        "db_selector_label": "Specify the data source to use",
        "header_expected_return": "Estimation Methods Configuration",
        "subheader_expected_return": "Expected Return",
        "select_method_expected_return": "Estimation Method",
        "select_bandwidth_method": "Method for calculating the number of observations used (bandwidth)",
        "input_bandwidth_value": "Set the bandwidth",
        "slider_lambda": "Select $$\\lambda$$",
        "expander_simple": "Expected Return Estimation Method: **Simple**",
        "expander_simple_text": r"""
        This method defines the expected return of asset $i$ as
        $$
        \hat{\mu}_i = \frac{1}{T} \sum_{t=0}^{T} R_{i,t}.
        $$
        """,
        "expander_ewma": "Expected Return Estimation Method: **Exponential Moving Average**",
        "expander_ewma_text": r"""
        This method defines the return of asset $i$ as
        $$
        \hat{\mu}_i = (1-\lambda) \sum_{t=0}^{T} \lambda^{T-t} R_{i,t}.
        $$
        """,
        "expander_barlett": "Expected Return Estimation Method: **Barlett Kernel**",
        "expander_barlett_text": r"""
        This method defines the return of asset $i$ as

        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Where $w_t$ is the Barlett kernel defined as

        $$
        w_t = \frac{t}{T}.
        $$
        """,
        "expander_parzen": "Expected Return Estimation Method: **Parzen Kernel**",
        "expander_parzen_text": r"""
        This method defines the return of asset $i$ as

        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Where $w_t$ is the Parzen kernel defined as:
        $$
        w_t =
        \begin{cases}
        1 - 6 \left( \frac{t}{T} \right)^{2} + 6 \left( \frac{t}{T} \right)^{3}, & \text{if } t \le \lfloor \frac{T}{2} \rfloor \\[2mm]
        2 \left( 1 - \frac{t}{T} \right)^{3}, & \text{if } t > \lfloor \frac{T}{2} \rfloor
        \end{cases}.
        $$
        """,
        "expander_tuckey": "Expected Return Estimation Method: **Tukey-Hanning**",
        "expander_tuckey_text": r"""
        This method defines the return of asset $i$ as

        $$
        \hat{\mu}_i = \sum_{t=0}^{T} w_t R_{i,t}
        $$

        Where $w_t$ is the Tukey-Hanning kernel defined as:

        $$
        w_t = \frac{1}{2} \left( 1 + \cos\left( \frac{\pi t}{T} \right) \right)
        $$
        """,
        "expander_trim": "Expected Return Estimation Method: **Trimmed Mean**",
        "expander_trim_text": r"""
        The trimmed mean estimates the expected return of asset $i$
        as the mean of daily returns excluding extreme percentiles (e.g., 5% and 95%):

        $$
        \hat{\mu}_i = \frac{1}{|S_i|} \sum_{t \in S_i} R_{i,t}, \quad
        S_i = \{ t : R_{i,t} \in [P_{5\%}, P_{95\%}] \}
        $$
        """,
        "expander_wins": "Expected Return Estimation Method: **Winsorized Mean**",
        "expander_wins_text": r"""
        The winsorized mean defines the expected return of asset $i$
        by replacing extremes with percentiles before calculating the mean:

        $$
        \hat{\mu}_i = \frac{1}{T} \sum_{t=0}^{T} \tilde{R}_{i,t}, \quad
        \tilde{R}_{i,t} =
        \begin{cases}
        P_{5\%}, & \text{if } R_{i,t} < P_{5\%} \\
        R_{i,t}, & \text{if } P_{5\%} \le R_{i,t} \le P_{95\%} \\
        P_{95\%}, & \text{if } R_{i,t} > P_{95\%}
        \end{cases}
        $$
        """,
        "expander_shrinkage": "Expected Return Estimation Method: **Shrinkage Mean Estimator**",
        "expander_shrinkage_text": r"""
        With shrinkage, the expected return is calculated by combining the historical mean of each asset
        with the overall mean of all assets, weighted by a factor $\lambda$:
        
        $$
        \hat{\mu}_i^{\text{shrink}} = \lambda \hat{\mu}_i^{\text{hist}} + (1-\lambda) \bar{\mu}
        $$

        Where:

        - $\hat{\mu}_i^{\text{hist}}$ is the historical mean of asset $i$ returns  
        - $\bar{\mu}$ is the mean return of all assets  
        - $\lambda \in [0,1]$ is the shrinkage factor
        """,
        "expander_newey_west_bandwidth": "Optimal Number of Observations Selection: **Newey–West**",
        "expander_newey_west_bandwidth_text": r"""
        The bandwidth is calculated as:

        $$
        B = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
        $$

        where $T$ is the total number of returns in the series.
        """,
        "expander_andrews_plugin_bandwidth": "Optimal Number of Observations Selection: **Andrews Rule**",
        "expander_andrews_plugin_bandwidth_text": r"""
        The bandwidth is calculated as:

        $$
        B = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
        $$

        where $T$ is the total number of returns in the series.
        """,
        "subheader_covariance_matrix": "Covariance Matrix",
        "select_method_covariance": "Estimation Method",
        "select_cov_bandwidth_method": "Lag Calculation Method",
        "input_cov_bandwidth_value": "Number of lags (L)",
        "expander_cov_simple": "Covariance Estimation Method: **Simple**",
        "expander_cov_simple_text": r"""
        This method considers the covariance matrix $$\Sigma$$ such that

        $$
        \Sigma_{i,j} = Cov(R_i, R_j).
        $$
        """,
        "expander_cov_newey": "Covariance Estimation Method: **Newey-West**",
        "expander_cov_newey_text": r"""
        This method estimates the covariance matrix accounting for
        autocorrelation up to a certain number of lags $$L$$.

        $$
        \Sigma = \sum_{t=0}^{L} w_t \, \Sigma_t.
        $$

        Where $w_t$ is the Barlett kernel:

        $$
        w_t = \frac{L - t}{L}
        $$

        and $$\Sigma_{t}$$ is the covariance matrix between current returns
        and returns lagged by $$t$$ periods.
        """,
        "expander_newey_west_lags": "Optimal Number of Lags Selection: **Newey–West**",
        "expander_newey_west_lags_text": r"""
        The number of lags used is calculated as:

        $$
        L = \left\lfloor 4 \left( \frac{T}{100} \right)^{\frac{2}{9}} \right\rfloor,
        $$

        where $T$ is the total number of returns in the series.
        """,
        "expander_andrews_plugin_lags": "Optimal Number of Lags Selection: **Andrews Rule**",
        "expander_andrews_plugin_lags_text": r"""
        The number of lags used is calculated as:

        $$
        L = \left\lfloor 1.2 \, T^{\frac{1}{3}} \right\rfloor,
        $$

        where $T$ is the total number of returns in the series.
        """,
        "header_efficient_frontier": "Efficient Frontier Size Configuration",
        "input_efficient_n_steps": "Number of portfolios to calculate on the efficient frontier"
    }
}

translations_efficient_frontier = {
    "es": {
        "page_title": "Frontera eficiente",
        "subheader_frontier": "Frontera eficiente",
        "frontier_description_1": (
            "El gráfico que ves a continuación representa el **mínimo riesgo** que se puede obtener "
            "en una cartera compuesta por los activos seleccionados para cada valor de rentabilidad posible."
        ),
        "frontier_description_2": (
            "Mueve el **selector** para ver qué cartera proporciona cada combinación de **rentabilidad / riesgo**."
        ),
        "slider_selected_portfolio": "Cartera seleccionada",
        "subheader_additional_portfolios": "Carteras adicionales",
        "toggle_individual_assets": "Activos individuales",
        "toggle_individual_assets_help": "Mostrar las carteras formadas por un único activo",
        "toggle_custom_portfolios": "Carteras personalizadas",
        "toggle_custom_portfolios_help": "Crear nuevas carteras personalizadas",
        "custom_portfolio_caption": (
            "Configura nuevas carteras especificando su nombre y el peso de cada activo. "
            "Los pesos se normalizarán automáticamente."
        ),
        "subheader_selected_portfolio": "Cartera seleccionada",
        "trace_frontier": "Frontera eficiente",
        "trace_selected_portfolio": "Cartera seleccionada",
        "trace_individual_portfolios": "Carteras de un activo",
        "trace_custom_portfolios": "Carteras personalizadas",
        "xaxis_risk": "Riesgo anual",
        "yaxis_return": "Rentabilidad (%)",
        "custom_portfolio_column_name": "Nombre",
        "error_assets_not_defined": "¡Error! Debes definir los activos primero"
    },
    "en": {
        "page_title": "Efficient Frontier",
        "subheader_frontier": "Efficient Frontier",
        "frontier_description_1": (
            "The chart below represents the **minimum risk** achievable "
            "for a portfolio composed of the selected assets for each possible return value."
        ),
        "frontier_description_2": (
            "Move the **slider** to see which portfolio provides each **return / risk** combination."
        ),
        "slider_selected_portfolio": "Selected portfolio",
        "subheader_additional_portfolios": "Additional portfolios",
        "toggle_individual_assets": "Individual assets",
        "toggle_individual_assets_help": "Show portfolios composed of a single asset",
        "toggle_custom_portfolios": "Custom portfolios",
        "toggle_custom_portfolios_help": "Create new custom portfolios",
        "custom_portfolio_caption": (
            "Configure new portfolios by specifying their name and the weight of each asset. "
            "Weights will be normalized automatically."
        ),
        "subheader_selected_portfolio": "Selected portfolio",
        "trace_frontier": "Efficient Frontier",
        "trace_selected_portfolio": "Selected Portfolio",
        "trace_individual_portfolios": "Single-asset portfolios",
        "trace_custom_portfolios": "Custom portfolios",
        "xaxis_risk": "Annual Risk",
        "yaxis_return": "Return (%)",
        "custom_portfolio_column_name": "Name",
        "error_assets_not_defined": "Error! You must define the assets first"
    }
}

translations_general = {
    "es": {
        "home_navbar": "Inicio",
        "asset_selection_navbar": "Selección de activos",
        "efficient_frontier_navbar": "Frontera eficiente",
        "config_navbar": "Configuración"
    },
    "en": {
        "home_navbar": "Home",
        "asset_selection_navbar": "Asset Selection",
        "efficient_frontier_navbar": "Efficient Frontier",
        "config_navbar": "Configuration"
    }
}