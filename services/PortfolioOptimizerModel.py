from services.ReturnsCovarianceModel import ReturnsCovarianceModel
from services.Portfolio import Portfolio
import cvxpy as cp
import numpy as np
from typing import Tuple

class PortfolioOptimizerModel:
    def __init__(self, returns_covariance_model: ReturnsCovarianceModel):
        self._ret_cov_model = returns_covariance_model

        self._min_variance_portfolio = None
        self._max_variance_portfolio = None

        self._min_return_portfolio = None
        self._max_return_portfolio = None

        self._efficient_frontier = None

        self._individual_portfolios = None
        
        if not self._ret_cov_model.PSD:
            raise ValueError(f"Returns covariance matrix must be PSD (positive semidefinite)")

    @property
    def returns_covariance_model(self):
        return self._ret_cov_model
        
    @property
    def n_assets(self):
        return self.returns_covariance_model.n_assets
    
    
    @property
    def assets(self):
        return self.returns_covariance_model.assets
    
    @property
    def min_variance_portfolio(self, verbose : bool = False) -> Portfolio:
        if self._min_variance_portfolio is not None:
            return self._min_variance_portfolio

        w = cp.Variable(self.n_assets)

        sigma = self.returns_covariance_model.covariance_matrix.values

        prob = cp.Problem(cp.Minimize(cp.quad_form(w, sigma)),
                [
                    cp.sum(w) == 1,
                    w >= 0
                ])
        
        prob.solve(solver=cp.ECOS)

        if prob.status not in ["optimal", "optimal_inaccurate"]:
            if verbose:
                print(f"Non feasible problem")
            return None
        
        self._min_variance_portfolio = Portfolio(self.returns_covariance_model, w.value)

        return self._min_variance_portfolio
    
    # @property
    # def max_variance_portfolio(self) -> Portfolio.Portfolio:
    #     if self._max_variance_portfolio is not None:
    #         return self._max_variance_portfolio
        
    #     sigma = self.returns_covariance_model.covariance_matrix.values

    #     variances = np.diag(sigma)

    #     id_max = np.argmax(variances)
    #     weights = np.zeros_like(variances)
    #     weights[id_max] = 1.0
        
    #     self._max_variance_portfolio = Portfolio.Portfolio(self.returns_covariance_model, weights)

    #     return self._max_variance_portfolio
    
    @property#NO IMPONGO QUE SEA POSITIVO
    def max_variance_portfolio(self) -> Portfolio:
        if self._max_variance_portfolio is not None:
            return self._max_variance_portfolio

        sigma = self.returns_covariance_model.covariance_matrix.values
        _, eigvecs = np.linalg.eigh(sigma)

        # autovector correspondiente al mayor autovalor
        w_max = eigvecs[:, -1]
        # normalizar para que sume 1
        w_max = w_max / np.sum(w_max)

        self._max_variance_portfolio = Portfolio(self.returns_covariance_model, w_max)
        return self._max_variance_portfolio
    
    @property
    def min_return_portfolio(self) -> Portfolio:
        if self._min_return_portfolio is not None:
            return self._min_return_portfolio
        
        returns = self.returns_covariance_model.expected_returns.values

        id_max = np.argmin(returns)
        weights = np.zeros_like(returns)
        weights[id_max] = 1.0
        
        self._min_return_portfolio = Portfolio(self.returns_covariance_model, weights)

        return self._min_return_portfolio
    
    @property
    def max_return_portfolio(self) -> Portfolio:
        if self._max_return_portfolio is not None:
            return self._max_return_portfolio
        
        returns = self.returns_covariance_model.expected_returns.values

        id_max = np.argmax(returns)
        weights = np.zeros_like(returns).reshape(-1)
        weights[id_max] = 1.0
        
        self._max_return_portfolio = Portfolio(self.returns_covariance_model, weights)

        return self._max_return_portfolio
    
    def min_variance_portfolio_given_daily_return(self, daily_return : float, verbose : bool = False) -> Portfolio:
        w = cp.Variable(self.n_assets)

        sigma = self.returns_covariance_model.covariance_matrix.values
        mu = self.returns_covariance_model.expected_returns.values.flatten()

        prob = cp.Problem(
            cp.Minimize(cp.quad_form(w, sigma)),
            [
                w.T @ mu >= daily_return,
                cp.sum(w) == 1,
                w >= 0
            ]
        )

        prob.solve(solver=cp.ECOS)

        if prob.status not in ["optimal", "optimal_inaccurate"]:
            if verbose:
                print(f"Non feasible problem for expected daily return: {daily_return}")
            return None

        return Portfolio(self.returns_covariance_model, w.value)
    
    def min_variance_portfolio_given_annual_return(self, annual_return : float, verbose : bool = False) -> Portfolio:
        return self.min_variance_portfolio_given_daily_return(daily_return=self._deannualize_return(annual_return), verbose=verbose)
    
    def max_return_portfolio_given_daily_variance(self, daily_variance : float, verbose : bool = False) -> Portfolio:
        w = cp.Variable(self.n_assets)

        sigma = self.returns_covariance_model.covariance_matrix.values
        mu = self.returns_covariance_model.expected_returns.values.flatten()

        prob = cp.Problem(cp.Maximize(w.T@mu),
                [
                    cp.quad_form(w, sigma) <= daily_variance, 
                    cp.sum(w) == 1,
                    w >= 0
                ])

        prob.solve(solver=cp.ECOS)

        if prob.status not in ["optimal", "optimal_inaccurate"]:
            if verbose:
                print(f"Non feasible problem for expected daily variance: {daily_variance}")
            return None

        return Portfolio(self.returns_covariance_model, w.value)
    
    def max_return_portfolio_given_annual_variance(self, annual_variance : float, verbose : bool = False) -> Portfolio:
        return self.max_return_portfolio_given_daily_variance(daily_variance=self._deannualize_variance(annual_variance), verbose=verbose)

    def max_return_portfolio_given_daily_risk(self, daily_risk : float, verbose : bool = False) -> Portfolio:
        return self.max_return_portfolio_given_daily_variance(daily_variance=self._risk_to_var(daily_risk), verbose=verbose)
    
    def max_return_portfolio_given_annual_risk(self, annual_risk : float, verbose : bool = False) -> Portfolio:
        return self.max_return_portfolio_given_daily_variance(daily_variance=self._deannualize_variance(self._risk_to_var(annual_risk)), verbose=verbose)

    @property
    def efficient_frontier(self) -> list[Portfolio]:
        if self._efficient_frontier is None:
            self.calculate_efficient_frontier()

        return self._efficient_frontier
    
    @property
    def individual_portfolios(self) -> list[Portfolio]:
        if self._individual_portfolios is not None:
            return self._individual_portfolios

        individual_portfolios = []

        for i in range(self.n_assets):
            w = np.array([1 if i == j else 0 for j in range(self.n_assets)])

            name = self.assets.asset_name[i]

            individual_portfolios.append(Portfolio(self.returns_covariance_model, w, name))

        self._individual_portfolios = individual_portfolios

        return self._individual_portfolios

    def custom_portfolio(self, w: np.array, name: str = None) -> Portfolio:
        return Portfolio(self.returns_covariance_model, w, name)


    def calculate_efficient_frontier(self, n_steps=20, verbose=False) -> list[Portfolio]:
        min_var_portfolio = self.min_variance_portfolio
        max_ret_portfolio = self.max_return_portfolio

        #AQUI COMPROBAMOS SI LA DIFERENCIA DE WEIGHTS ES IDÉNTICA (O CASI) Y SI ES ASÍ LA FRONTERA EFICIENTE CONTIENE EL MISMO PORTFOLIO N_STEPS

        if np.linalg.norm(min_var_portfolio.weights - max_ret_portfolio.weights) < 0.05:
            self._efficient_frontier = [min_var_portfolio]*n_steps
            return self._efficient_frontier

        min_var = min_var_portfolio.daily_variance
        max_var = max_ret_portfolio.daily_variance

        if min_var == max_var:
            raise ValueError(f"min_var and max_var are the same")

        efficient_frontier = []

        step = (max_var-min_var)/n_steps

        for i in range(n_steps+1):
            target_daily_variance = min_var + i*step

            portfolio = self.max_return_portfolio_given_daily_variance(daily_variance=target_daily_variance, verbose=True)

            efficient_frontier.append(portfolio)

        self._efficient_frontier = efficient_frontier

        return self._efficient_frontier


    # def calculate_efficient_frontier(self, n_steps=20, verbose=False, annual_steps = True) -> list[Portfolio.Portfolio]:
    #     if annual_steps:
    #         min_risk = self.min_return_portfolio.annual_expected_return
    #         max_return = self.max_return_portfolio.annual_expected_return
    #     else:
    #         min_return = self.min_return_portfolio.daily_expected_return
    #         max_return = self.max_return_portfolio.daily_expected_return

    #     if min_return == max_return:
    #         raise ValueError(f"min_returns and max_returns are the same")

    #     efficient_frontier = []

    #     step = (max_return-min_return)/n_steps

    #     for i in range(n_steps+1):
    #         target_return = min_return + i*step

    #         if annual_steps:
    #             print(target_return)
    #             portfolio = self.min_variance_portfolio_given_annual_return(annual_return=target_return, verbose=verbose)
                
    #             print(portfolio.annual_expected_return)
    #         else:
    #             portfolio = self.min_variance_portfolio_given_daily_return(daily_return=target_return, verbose=verbose)

    #         efficient_frontier.append(portfolio)

    #     self._efficient_frontier = efficient_frontier

    #     return self._efficient_frontier

    def max_annual_sharpe_ratio_portfolio(self, annual_risk_free: float = 0.2) -> Portfolio:
        max_sharpe_porfolio = None
        max_sharpe = None

        for portfolio in self.efficient_frontier:
            if max_sharpe_porfolio is None:
                max_sharpe_porfolio = portfolio
                max_sharpe = portfolio.annual_sharpe_ratio(annual_risk_free = annual_risk_free)
                continue

            if new_sharpe := portfolio.annual_sharpe_ratio(annual_risk_free = annual_risk_free) > max_sharpe:
                max_sharpe_porfolio = portfolio
                max_sharpe = new_sharpe
                
        return max_sharpe_porfolio
    
    def max_daily_sharpe_ratio_portfolio(self, daily_risk_free: float = 0.2) -> Portfolio:
        max_sharpe_porfolio = None
        max_sharpe = None

        for portfolio in self.efficient_frontier:
            if max_sharpe_porfolio is None:
                max_sharpe_porfolio = portfolio
                max_sharpe = portfolio.daily_sharpe_ratio(daily_risk_free = daily_risk_free)
                continue

            if new_sharpe := portfolio.daily_sharpe_ratio(daily_risk_free = daily_risk_free) > max_sharpe:
                max_sharpe_porfolio = portfolio
                max_sharpe = new_sharpe
                
        return max_sharpe_porfolio

    def _annualize_return(self, daily_return: float):
        return (1+daily_return)**252 - 1
    
    def _deannualize_return(self, year_return: float):
        return (1+year_return)**(1/252) - 1
    
    def _annualize_variance(self, daily_variance: float):
        return daily_variance*252
    
    def _deannualize_variance(self, year_variance: float):
        return year_variance/252
    
    def _annualize_risk(self, daily_risk: float):
        return daily_risk*np.sqrt(252)
    
    def _deannualize_risk(self, year_risk: float):
        return year_risk/np.sqrt(252)
    
    def _var_to_risk(self, var:float):
        return var**0.5
    
    def _risk_to_var(self, risk:float):
        return risk**2