from services.MarketData_V2 import MarketData_V2
from enum import Enum
import numpy as np
import pandas as pd

class ReturnsCovarianceModel:
    class CovarianceMethod(str, Enum):
        SIMPLE = 'Simple covariance estimator'
        NEWEY_WEST = 'Newey West estimator'

    class WeightingMethod(str, Enum):
        CONSTANT = 'Constant method'
        BARLETT = 'Barlett method'
        EXPONENTIAL = 'Exponential method'
        PARZEN = 'Parzen method'
        TUKEY_HANNING = 'Tukey-Hanning method'


    class ExpectedReturnEstimationMethod(str, Enum):
        SIMPLE = 'Simple expected return estimation method'
        WHM_EWMA = 'Weighted historical mean: Exponential weighted moving average'
        WHM_BARLETT = 'Weighted historical mean: Barlett method'
        WHM_PARZEN = 'Weighted historical mean: Parzen method'
        WHM_TUKEY_HANNING = 'Weighted historical mean: Tukey-Hanning method'
        WHM_TRIM = 'Weighted historical mean: Trimmed mean'
        WHM_WINS = 'Weighted historical mean: Winsorized mean'
        SHRINKAGE = 'Shrinkage method with asset return average'

    class BandwidthMethod(str, Enum):
        NEWEY_WEST_RULE_OF_THUMB = 'Newey West rule'
        ANDREWS_PLUGIN = 'Andrews rule (C=1.2)'
        ALL = 'Use all values'
        MANUAL = 'Set bandwidth manually'

    def __init__(self, market_data: MarketData_V2):
        if len(market_data.active_assets) < 2:
            raise ValueError(f"Market Data object must contain at least 2 active assets")
        
        self._market_data = market_data

        self._expected_returns = None
        self._covariance_matrix = None
        self._correlation_matrix = None

    @property
    def market_data(self):
        return self._market_data

    @property
    def expected_returns(self):
        if self._expected_returns is not None:
            return self._expected_returns

        return self.estimate_expected_returns()
    
    @property
    def returns_len(self):
        return self.market_data.returns_len
    
    @property
    def n_assets(self):
        return self.market_data.n_active_assets
    
    @property
    def assets(self):
        return self.market_data.active_assets

    def estimate_expected_returns(self, estimation_method : ExpectedReturnEstimationMethod = ExpectedReturnEstimationMethod.SIMPLE, bandwidth_method: BandwidthMethod | None = BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, bandwidth_value : int | None = 10, lmb: float | None = 0.5) -> pd.DataFrame:
        if estimation_method not in (ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE) and bandwidth_method is None:
            raise ValueError(f"Bandwidth method cant be None for selected expected return estimation method, selected: {estimation_method}")
        
        if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL and (bandwidth_value is None or bandwidth_value <= 0 or bandwidth_value >= self._market_data.returns_len - 1):
            raise ValueError(f"Bandwidth must be between 0 and returns_df length")

        if lmb is not None and (lmb < 0 or lmb > 1):
            raise ValueError(f"lmb must be a float in the interval [0,1]")

        if estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE:

            self._expected_returns = self._market_data.returns_df.mean()
            self._expected_returns = self._expected_returns.to_frame('expected_return')
            self._expected_returns.index.name = 'asset'
            return self._expected_returns
        
        elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.SHRINKAGE:
            self._expected_returns = self._market_data.returns_df.mean()
            self._expected_returns = self._expected_returns.to_frame('expected_return')
            self._expected_returns.index.name = 'asset'

            asset_average_return =  self._expected_returns.mean()

            self._expected_returns = self._expected_returns * lmb + asset_average_return * (1 - lmb)

            return self._expected_returns
        
        else:
            if bandwidth_method != ReturnsCovarianceModel.BandwidthMethod.MANUAL:
                bandwidth_value = self._bandwidth(T=self._market_data.returns_len, bandwidth_method=bandwidth_method)

            L = bandwidth_value
        
            if estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TRIM:
                tmp = self._market_data.returns_df[-L:]

                P_05 = tmp.quantile(0.05)
                P_95 = tmp.quantile(0.95)

                tmp = tmp[(tmp > P_05)]
                tmp = tmp[(tmp < P_95)]

                self._expected_returns = tmp.mean()
                self._expected_returns = self._expected_returns.to_frame('expected_return')
                self._expected_returns.index.name = 'asset'
                return self._expected_returns

            elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_WINS:
                tmp = self._market_data.returns_df[-L:]

                P_05 = tmp.quantile(0.05)
                P_95 = tmp.quantile(0.95)

                tmp = tmp.clip(lower=P_05, upper=P_95, axis=1)

                self._expected_returns = tmp.mean()
                self._expected_returns = self._expected_returns.to_frame('expected_return')
                self._expected_returns.index.name = 'asset'
                return self._expected_returns

            else:
                if estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_EWMA:

                    w = [(1-lmb)*lmb**(L-t) for t in range(0, L)]

                elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_BARLETT:

                    w = [1-t/L for t in range(0, L)]

                elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_PARZEN:

                    mid = int(np.floor(L/2))

                    w_1 = [1 - 6*(t/L)**2 + 6*(t/L)**3 for t in range(0, mid + 1)]
                    w_2 = [2*(1 - t/L)**3 for t in range(mid + 1, L)]

                    w = w_1 + w_2

                elif estimation_method == ReturnsCovarianceModel.ExpectedReturnEstimationMethod.WHM_TUKEY_HANNING:
                    
                    w = [(1/2)*(1 + np.cos(np.pi * t / L)) for t in range(0, L)]

                else:
                    raise ValueError(f"ExpectedReturnEstimationMethod method not implemented")
                
                w = w/np.sum(w)
                w = w[::-1] #nuestros pesos están en orden inverso a nuestros registros

                prod = self._market_data.returns_df[-L:].mul(w, axis = 0)

                self._expected_returns = np.sum(prod, axis = 0)
                self._expected_returns = self._expected_returns.to_frame('expected_return')
                self._expected_returns.index.name = 'asset'
                return self._expected_returns
    
    @property
    def covariance_matrix(self):
        if self._covariance_matrix is not None:
            return self._covariance_matrix

        return self.estimate_covariance_matrix()
    
    @property
    def PSD(self):
        eigvals = np.linalg.eigvals(self.covariance_matrix.values)
        return (eigvals >= 0).all()

    def _reset_correlation_matrix(self):
        self._correlation_matrix = None

    def force_PSD(self, tolerance = 1e-5):
        if self._covariance_matrix is not None:
            sigma = self._covariance_matrix.values
            eigvals, eigvec = np.linalg.eig(sigma)

            # Ajustar valores propios (clamping)
            eigvals_adj = [x if abs(x) > tolerance else 0 for x in eigvals]

            # Reconstruir matriz
            sigma_adj = eigvec @ np.diag(eigvals_adj) @ eigvec.T

            # Crear nuevo DataFrame con mismos índices y columnas
            matrix_adj = pd.DataFrame(
                sigma_adj,
                index=self._covariance_matrix.index,
                columns=self._covariance_matrix.columns
            )

            self._covariance_matrix = matrix_adj

    def estimate_covariance_matrix(self, covariance_method=CovarianceMethod.SIMPLE, bandwidth_method: BandwidthMethod | None = BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, bandwidth_value: int | None = 10, weighting_method: WeightingMethod | None = WeightingMethod.CONSTANT, lmb: float | None = 0.5) -> pd.DataFrame:   
        if covariance_method == ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST and bandwidth_method is None:
            raise ValueError(f"Bandwidth method can't be None for selected covariance method, selected: {covariance_method}")
        
        if covariance_method == ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST and weighting_method is None:
            raise ValueError(f"Weighting method can't be None for selected covariance method, selected: {covariance_method}")

        if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.MANUAL and (bandwidth_value is None or bandwidth_value <= 0 or bandwidth_value >= self._market_data.returns_len - 1):
            raise ValueError(f"Bandwidth must be between 0 and returns_df length, given {bandwidth_value}")

        if weighting_method == ReturnsCovarianceModel.WeightingMethod.EXPONENTIAL and lmb is None:
            raise ValueError(f"lambda can't be None for selected weighting method, selected: {weighting_method}")

        if lmb is not None and (lmb < 0 or lmb > 1):
            raise ValueError(f"lmb must be a float in the interval [0,1]")

        self._reset_correlation_matrix()

        if covariance_method == ReturnsCovarianceModel.CovarianceMethod.SIMPLE:
            self._covariance_matrix = self._market_data.returns_df.cov()
            self._covariance_matrix.index.name = 'covariance'
            self._covariance_matrix.columns.name = 'covariance'
            return self._covariance_matrix
        elif covariance_method == ReturnsCovarianceModel.CovarianceMethod.NEWEY_WEST:
            lags = 0

            if bandwidth_method != ReturnsCovarianceModel.BandwidthMethod.MANUAL:
                bandwidth_value = self._bandwidth(T=self._market_data.returns_len, bandwidth_method=bandwidth_method)

            lags = bandwidth_value

            df_returns_mean = self._market_data.returns_df.mean()

            self._covariance_matrix = self._market_data.returns_df.cov()

            for k in range(1, lags+1):
                w = self._weight(k=k, m=lags, lmb=lmb, weighting_method=weighting_method)

                lagged_cov = self._lagged_cov(self._market_data.returns_df, k, df_returns_mean)
                

                self._covariance_matrix = self._covariance_matrix + w*(lagged_cov + lagged_cov.T)

            self._covariance_matrix.index.name = 'covariance'
            self._covariance_matrix.columns.name = 'covariance'
            return self._covariance_matrix
        else:
            raise ValueError(f"CovarianceMethod method not implemented")
    
    @property
    def correlation_matrix(self) -> pd.DataFrame:
        if self._correlation_matrix is not None:
            return self._correlation_matrix
        
        D = pd.DataFrame(np.diag(self.covariance_matrix))
        var_matrix = pd.DataFrame(np.dot(D, D.T))
        var_matrix = var_matrix**0.5

        var_matrix.index = self.covariance_matrix.index
        var_matrix.columns = self.covariance_matrix.index

        aux = self.covariance_matrix.copy()

        self._correlation_matrix = aux/var_matrix
        self._correlation_matrix.index.name = 'correlation'
        self._correlation_matrix.columns.name = 'correlation'
        return self._correlation_matrix
    
    def _bandwidth(self, T: int, bandwidth_method: BandwidthMethod):
        if bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB:
            return int(np.floor(4 * (T/100)**(2/9)))
        elif bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ANDREWS_PLUGIN:
            return int(np.floor(1.2 * T**(1/3)))
        elif bandwidth_method == ReturnsCovarianceModel.BandwidthMethod.ALL:
            return T-1
        else:
            raise ValueError(f"Bandwidth method not implemented")
    
    def _weight(self, k: int, m: int, lmb: float | None, weighting_method: WeightingMethod):
        if weighting_method == ReturnsCovarianceModel.WeightingMethod.CONSTANT:
            return 1
        elif weighting_method == ReturnsCovarianceModel.WeightingMethod.BARLETT:
            return 1 - k/(m+1)
        elif weighting_method == ReturnsCovarianceModel.WeightingMethod.EXPONENTIAL:
            return lmb**k
        elif weighting_method == ReturnsCovarianceModel.WeightingMethod.PARZEN:
            if 0 <= k and k <= m/2:
                return 1 - 6*(k/m)**2 + 6*(k/m)**3
            else:
                return 2*(1-k/m)**3
        elif weighting_method == ReturnsCovarianceModel.WeightingMethod.TUKEY_HANNING:
            return (1/2)*(1 + np.cos(np.pi*k/m))
        else:
            raise ValueError(f"WeightingMethod method not implemented, given {weighting_method}")
    
    def _lagged_cov(self, df:pd.DataFrame, lag:int, df_mean: pd.Series = None) -> pd.DataFrame:
        df_lag = df.shift(lag)

        cols = df_lag.columns

        if df_mean is None:
            df_mean = df.mean()

        A = (df-df_mean).astype(np.float64)
        B = (df_lag-df_mean).astype(np.float64)

        if lag > 0:
            A = A[lag:]
            B = B.dropna()
        elif lag < 0:
            A = A[:lag]
            B = B.dropna()

        cov = pd.DataFrame(np.dot(A.T, B)/(len(A)-1))
        cov.index = cols
        cov.columns = cols

        return cov
