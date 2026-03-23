from abc import ABC, abstractmethod
from services.DataProvider import DataProvider
import pandas as pd
import numpy as np

class ReturnsCovarianceModel(ABC):

    def __init__(self, data_provider: DataProvider):
        self._data_provider = data_provider

    @property
    def data_provider(self) -> DataProvider:
        return self._data_provider

    @property
    @abstractmethod
    def expected_returns(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def estimate_expected_returns(self):
        pass

    @property
    @abstractmethod
    def covariance_matrix(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def estimate_covariance_matrix(self):
        pass

    @property
    @abstractmethod
    def correlation_matrix(self) -> pd.DataFrame:
        pass

    #FUNCIONES FORWARDING

    @property
    def n_assets(self):
        return self.data_provider.n_assets
    
    @property
    def assets(self):
        return self.data_provider.assets
    
    @property
    def returns_len(self):
        return self.data_provider.returns_len
    
    @property
    def PSD(self):
        eigvals = np.linalg.eigvals(self.covariance_matrix.values)
        return (eigvals >= 0).all()
    
    def force_PSD(self, tolerance = 1e-5):
        if self._covariance_matrix is not None:
            sigma = self._covariance_matrix.values
            eigvals, eigvec = np.linalg.eig(sigma)

            # CLAMPEAMOS VALORES PROPIOS
            #eigvals_adj = [x if abs(x) > tolerance else 0 for x in eigvals]
            eigvals_adj = [x if x > tolerance else 0 for x in eigvals]

            # RECONSTRUIMOS LA MATRIZ A PARTIR DE LOS NUEVOS VALORES PROPIOS Y LOS VECTORES PROPIOS
            sigma_adj = eigvec @ np.diag(eigvals_adj) @ eigvec.T

            # CONSTRUIMOS LA NUEVA MATRIZ ASOCIADA
            matrix_adj = pd.DataFrame(
                sigma_adj,
                index=self._covariance_matrix.index,
                columns=self._covariance_matrix.columns
            )

            self._covariance_matrix = matrix_adj