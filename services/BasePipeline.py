from services.MarketData_V2 import MarketData_V2
from services.MarketDataProvider import MarketDataProvider
from services.SimpleReturnsCovarianceModel import SimpleReturnsCovarianceModel
from services.PortfolioOptimizerModel import PortfolioOptimizerModel
from services.Portfolio import Portfolio
import pandas as pd
import numpy as np


class BasePipeline():
    def __init__(self, market_data: MarketData_V2):
        self._market_data = market_data
        self._data_provider = MarketDataProvider(market_data=market_data)
        self._returns_cov_model = SimpleReturnsCovarianceModel(data_provider=self._data_provider)
        
        self._portfolio_optimizer_model = None
    
    @property
    def market_data(self):
        return self._market_data
    
    @property
    def real_returns(self):
        return self.market_data.returns_df

    @property
    def returns_len(self):
        return self._data_provider.returns_len
    
    @property
    def returns(self):
        return self._data_provider.returns
    
    @property
    def assets(self):
        return self._data_provider.assets
    
    @property
    def n_assets(self):
        return self._data_provider.n_assets
    
    def asset_name(self, asset: str):
        return self._data_provider.asset_name(asset)

    @property
    def returns_cov_model(self):
        return self._returns_cov_model

    def estimate_expected_returns(
            self, 
            estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value : int | None = 10, 
            lmb: float | None = 0.5
            ):
        
        self.returns_cov_model.estimate_expected_returns(
            estimation_method = estimation_method,
            bandwidth_method = bandwidth_method,
            bandwidth_value = bandwidth_value,
            lmb = lmb
        )

        self._reset_portfolio_optimizer_model()

    def estimate_covariance_matrix(
            self, 
            covariance_method : SimpleReturnsCovarianceModel.CovarianceMethod = SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value: int | None = 10, 
            weighting_method: SimpleReturnsCovarianceModel.WeightingMethod | None = SimpleReturnsCovarianceModel.WeightingMethod.CONSTANT, 
            lmb: float | None = 0.5
            ):
        
        self.returns_cov_model.estimate_covariance_matrix(
            covariance_method = covariance_method,
            bandwidth_method = bandwidth_method,
            bandwidth_value = bandwidth_value,
            weighting_method = weighting_method, 
            lmb = lmb
        )

        if not self.returns_cov_model.PSD:
            self.returns_cov_model.force_PSD()

        self._reset_portfolio_optimizer_model()

    @property
    def covariance_matrix(self) -> pd.DataFrame:
        return self.returns_cov_model.covariance_matrix
    
    @property
    def correlation_matrix(self) -> pd.DataFrame:
        return self.returns_cov_model.correlation_matrix
    
    @property
    def expected_returns(self) -> pd.DataFrame:
        return self.returns_cov_model.expected_returns

    def _reset_portfolio_optimizer_model(self):
        self._portfolio_optimizer_model = None

    #   CAMBIOS A HACER

    @property
    def portfolio_optimizer_model(self):
        if self._portfolio_optimizer_model is None:
            self._portfolio_optimizer_model = PortfolioOptimizerModel(self.returns_cov_model)

        return self._portfolio_optimizer_model

    def calculate_efficient_frontier(self, n_steps = 20):
        self.portfolio_optimizer_model.calculate_efficient_frontier(n_steps=n_steps)

    @property
    def efficient_frontier(self):
        return self.portfolio_optimizer_model.efficient_frontier
    
    @property
    def individual_portfolios(self):
        return self.portfolio_optimizer_model.individual_portfolios
    
    def custom_portfolio(self, w: np.array, name: str = None) -> Portfolio:
        return Portfolio(self.returns_cov_model, w, name)

