from services.SimpleReturnsCovarianceModel import ReturnsCovarianceModel
import numpy as np

class Portfolio:
    def __init__(self, returns_covariance_model: ReturnsCovarianceModel, weights: np.array, name :str = 'portfolio'):
        self._ret_cov_model = returns_covariance_model
        self._weights = weights

        self._calculate_values()

        self._daily_variance = None
        self._daily_risk = None
        self._daily_expected_return = None

        self._annual_variance = None
        self._annual_risk = None
        self._annual_expected_return = None

        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def return_covariance_model(self) -> ReturnsCovarianceModel:
        return self._ret_cov_model

    @property
    def assets(self):
        return self._ret_cov_model.assets

    @property
    def weights(self):
        return self._weights

    @property
    def daily_variance(self):
        if self._daily_variance is None:
            self._calculate_values()

        return self._daily_variance
    
    @property
    def annual_variance(self):
        if self._annual_variance is None:
            self._calculate_values()

        return self._annual_variance

    @property
    def daily_risk(self):
        if self._daily_risk is None:
            self._calculate_values()

        return self._daily_risk
    
    @property
    def annual_risk(self):
        if self._annual_risk is None:
            self._calculate_values()

        return self._annual_risk

    @property
    def daily_expected_return(self):
        if self._daily_expected_return is None:
            self._calculate_values()

        return self._daily_expected_return
    
    @property
    def annual_expected_return(self):
        if self._annual_expected_return is None:
            self._calculate_values()

        return self._annual_expected_return

    @property
    def annual_sharpe_ratio(self, annual_risk_free: float = 0.02):
        return (self.annual_expected_return - annual_risk_free) / self.annual_risk 

    @property
    def daily_sharpe_ratio(self, daily_risk_free: float = 0.02):
        return (self.daily_expected_return - daily_risk_free) / self.daily_risk 

    def _calculate_values(self):
        sigma = self._ret_cov_model.covariance_matrix.values
        mu = self._ret_cov_model.expected_returns.values.flatten()

        w = self.weights

        portfolio_variance = (w.T @ sigma @ w)
        portfolio_return = (w.T @ mu)
        portfolio_risk = self._var_to_risk(portfolio_variance)
        
        self._daily_variance = portfolio_variance
        self._daily_risk = portfolio_risk
        self._daily_expected_return = portfolio_return

        self._annual_variance = self._annualize_variance(portfolio_variance)
        self._annual_risk = self._annualize_risk(portfolio_risk)
        self._annual_expected_return = self._annualize_return(portfolio_return)

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