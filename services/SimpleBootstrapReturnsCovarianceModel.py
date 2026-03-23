from services.SimpleReturnsCovarianceModel import SimpleReturnsCovarianceModel
from services.ReturnsCovarianceModel import ReturnsCovarianceModel
from services.BlockBootstrapDataProvider import BlockBootstrapDataProvider
import pandas as pd
import numpy as np

class SimpleBootstrapReturnsCovarianceModel(ReturnsCovarianceModel):

    def __init__(self, data_provider: BlockBootstrapDataProvider):
        super().__init__(data_provider)

        self._models = [SimpleReturnsCovarianceModel(d_p) for d_p in data_provider.bootsrtap_samples]
        
        self._expected_returns = None
        self._covariance_matrix = None
        self._correlation_matrix = None

    @property
    def models(self):
        return self._models

    @property
    def expected_returns(self) -> pd.DataFrame:
        if self._expected_returns is None:
            returns = [rcv.expected_returns for rcv in self.models]

            self._expected_returns = pd.DataFrame(np.mean([matrix.values for matrix in returns], axis=0), index=returns[0].index, columns=returns[0].columns)

        return self._expected_returns

    def estimate_expected_returns(
            self, 
            estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value : int | None = 10, 
            lmb: float | None = 0.5
            ):
        
        for rcv in self.models:
            rcv.estimate_expected_returns(
                estimation_method = estimation_method,
                bandwidth_method = bandwidth_method,
                bandwidth_value = bandwidth_value,
                lmb = lmb
            )

        self._expected_returns = None

    @property
    def covariance_matrix(self) -> pd.DataFrame:
        if self._covariance_matrix is None:
            cov_matrix = [rcv.covariance_matrix for rcv in self.models]

            self._covariance_matrix = pd.DataFrame(np.mean([matrix.values for matrix in cov_matrix], axis=0), index=cov_matrix[0].index, columns=cov_matrix[0].columns)

        return self._covariance_matrix

    def estimate_covariance_matrix(
            self, 
            covariance_method : SimpleReturnsCovarianceModel.CovarianceMethod = SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value: int | None = 10, 
            weighting_method: SimpleReturnsCovarianceModel.WeightingMethod | None = SimpleReturnsCovarianceModel.WeightingMethod.CONSTANT, 
            lmb: float | None = 0.5
            ):
        
        for rcv in self.models:
            rcv.estimate_covariance_matrix(
                covariance_method = covariance_method,
                bandwidth_method = bandwidth_method,
                bandwidth_value = bandwidth_value,
                weighting_method = weighting_method, 
                lmb = lmb
            )

        self._covariance_matrix = None
        self._correlation_matrix = None

    @property
    def correlation_matrix(self) -> pd.DataFrame:
        if self._correlation_matrix is None:
            cor_matrix = [rcv.correlation_matrix for rcv in self.models]

            self._correlation_matrix = pd.DataFrame(np.mean([matrix.values for matrix in cor_matrix], axis=0), index=cor_matrix[0].index, columns=cor_matrix[0].columns)

        return self._correlation_matrix