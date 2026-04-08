from services.MarketData_V2 import MarketData_V2
from services.BlockBootstrapDataProvider import BlockBootstrapDataProvider
from services.MarketDataProvider import MarketDataProvider
from services.SimpleReturnsCovarianceModel import SimpleReturnsCovarianceModel
from services.SimpleBootstrapReturnsCovarianceModel import SimpleBootstrapReturnsCovarianceModel
from services.PortfolioOptimizerModel import PortfolioOptimizerModel
from services.Portfolio import Portfolio
import pandas as pd
import numpy as np

class BootstrapPipeline():
    def __init__(self, market_data: MarketData_V2, bootstrap_length = 100, block_length = 30):
        self._market_data = market_data
        market_data_provider = MarketDataProvider(market_data=market_data)

        self._data_provider = BlockBootstrapDataProvider(market_data_provider, bootstrap_length = bootstrap_length, block_length = block_length)

        self._return_cov_model = SimpleBootstrapReturnsCovarianceModel(data_provider=self._data_provider)
        
        self._portfolio_optimizer = None
        self._bootstrap_portfolio_optimizers = None

        self._calculated_efficient_frontier = False
        self._calculated_bootstrap_efficient_frontiers = False
    
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
    def return_cov_model(self):
        return self._return_cov_model

    def estimate_expected_returns(
            self, 
            estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value : int | None = 10, 
            lmb: float | None = 0.5
            ):
        
        self.return_cov_model.estimate_expected_returns(
            estimation_method = estimation_method,
            bandwidth_method = bandwidth_method,
            bandwidth_value = bandwidth_value,
            lmb = lmb
        )

        self._reset_portfolio_optimizer()

    def estimate_covariance_matrix(
            self, 
            covariance_method : SimpleReturnsCovarianceModel.CovarianceMethod = SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value: int | None = 10, 
            weighting_method: SimpleReturnsCovarianceModel.WeightingMethod | None = SimpleReturnsCovarianceModel.WeightingMethod.CONSTANT, 
            lmb: float | None = 0.5
            ):
        
        self.return_cov_model.estimate_covariance_matrix(
            covariance_method = covariance_method,
            bandwidth_method = bandwidth_method,
            bandwidth_value = bandwidth_value,
            weighting_method = weighting_method, 
            lmb = lmb
        )

        if not self.return_cov_model.PSD:
            self.return_cov_model.force_PSD()

        self._reset_portfolio_optimizer()

    @property
    def covariance_matrix(self) -> pd.DataFrame:
        return self.return_cov_model.covariance_matrix
    
    @property
    def correlation_matrix(self) -> pd.DataFrame:
        return self.return_cov_model.correlation_matrix
    
    @property
    def expected_returns(self) -> pd.DataFrame:
        return self.return_cov_model.expected_returns
    
    @property
    def covariance_matrix_stats(self) -> pd.DataFrame:
        return self.return_cov_model.covariance_matrix_stats
    
    @property
    def correlation_matrix_stats(self) -> pd.DataFrame:
        return self.return_cov_model.correlation_matrix_stats
    
    @property
    def expected_returns_stats(self) -> pd.DataFrame:
        return self.return_cov_model.expected_returns_stats

    @property
    def bootstrap_covariance_matrices(self):
        return [rcv.covariance_matrix for rcv in self.return_cov_model.models]
    
    @property
    def bootstrap_correlation_matrices(self):
        return [rcv.correlation_matrix for rcv in self.return_cov_model.models]
    @property
    def bootstrap_expected_returns(self):
        return [rcv.expected_returns for rcv in self.return_cov_model.models]

    def _reset_portfolio_optimizer(self):
        self._portfolio_optimizer = None
        self._bootstrap_portfolio_optimizers = None

        self._calculated_efficient_frontier = False
        self._calculated_bootstrap_efficient_frontiers = False

    @property
    def portfolio_optimizer(self):
        if self._portfolio_optimizer is None:
            self._portfolio_optimizer = PortfolioOptimizerModel(self.return_cov_model)

        return self._portfolio_optimizer

    @property
    def bootstrap_portfolio_optimizers(self):
        if self._bootstrap_portfolio_optimizers is None:
            self._bootstrap_portfolio_optimizers = [PortfolioOptimizerModel(rcv) for rcv in self.return_cov_model.models]

        return self._bootstrap_portfolio_optimizers

    def calculate_efficient_frontier(self, n_steps = 20):
        if self._calculated_efficient_frontier == False:
            self.portfolio_optimizer.calculate_efficient_frontier(n_steps=n_steps)
            self._calculated_efficient_frontier = True

    def calculate_bootstrap_efficient_frontiers(self, n_steps = 20):
        if self._calculated_bootstrap_efficient_frontiers == False:
            for opt in self.bootstrap_portfolio_optimizers:
                opt.calculate_efficient_frontier(n_steps=n_steps)

            self._calculated_bootstrap_efficient_frontiers = True

    @property
    def efficient_frontier(self):
        return self.portfolio_optimizer.efficient_frontier

    @property
    def bootstrap_efficient_frontiers(self):
        return [opt.efficient_frontier for opt in self.bootstrap_portfolio_optimizers]

    @property
    def individual_portfolios(self):
        return self.portfolio_optimizer.individual_portfolios
    
    def custom_portfolio(self, w: np.array, name: str = None) -> Portfolio:
        return Portfolio(self.return_cov_model, w, name)
    
    def bootstrap_portfolio_estimations(self, p: Portfolio):
        return [Portfolio(rcv, p.weights) for rcv in self.return_cov_model.models]

