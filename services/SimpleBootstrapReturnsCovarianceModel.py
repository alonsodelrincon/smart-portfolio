from services.SimpleReturnsCovarianceModel import SimpleReturnsCovarianceModel
from services.ReturnsCovarianceModel import ReturnsCovarianceModel
from services.BlockBootstrapDataProvider import BlockBootstrapDataProvider
import pandas as pd
import numpy as np
# import requests
# import concurrent.futures
# import threading

class SimpleBootstrapReturnsCovarianceModel(ReturnsCovarianceModel):

    def __init__(self, data_provider: BlockBootstrapDataProvider):
        super().__init__(data_provider)

        self._models = [SimpleReturnsCovarianceModel(d_p) for d_p in data_provider.bootsrtap_samples]
        
        self._expected_returns_stats = None
        self._covariance_matrix_stats = None
        self._correlation_matrix_stats = None

    @property
    def models(self):
        return self._models
    
    def _matrix_stats(self, matrix_list):
        stats = {
            'mean': pd.DataFrame(np.mean([matrix.values for matrix in matrix_list], axis=0), index=matrix_list[0].index, columns=matrix_list[0].columns),
            'std': pd.DataFrame(np.std([matrix.values for matrix in matrix_list], axis=0), index=matrix_list[0].index, columns=matrix_list[0].columns),
            'median': pd.DataFrame(np.median([matrix.values for matrix in matrix_list], axis=0), index=matrix_list[0].index, columns=matrix_list[0].columns),
            'p5': pd.DataFrame(np.percentile([matrix.values for matrix in matrix_list], 5, axis=0), index=matrix_list[0].index, columns=matrix_list[0].columns),
            'p95': pd.DataFrame(np.percentile([matrix.values for matrix in matrix_list], 95, axis=0), index=matrix_list[0].index, columns=matrix_list[0].columns)
        }

        return stats

    @property
    def expected_returns_stats(self):
        if self._expected_returns_stats is None:
            matrix_list = [rcv.expected_returns for rcv in self.models]

            self._expected_returns_stats = self._matrix_stats(matrix_list)

        return self._expected_returns_stats

    @property
    def covariance_matrix_stats(self):
        if self._covariance_matrix_stats is None:
            matrix_list = [rcv.covariance_matrix for rcv in self.models]

            self._covariance_matrix_stats = self._matrix_stats(matrix_list)

        return self._covariance_matrix_stats
    
    @property
    def correlation_matrix_stats(self):
        if self._correlation_matrix_stats is None:
            matrix_list = [rcv.correlation_matrix for rcv in self.models]

            self._correlation_matrix_stats = self._matrix_stats(matrix_list)

        return self._correlation_matrix_stats

    @property
    def expected_returns(self) -> pd.DataFrame:
        return self.expected_returns_stats['mean']

    # def estimate_expected_returns(
    #         self, 
    #         estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
    #         bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
    #         bandwidth_value : int | None = 10, 
    #         lmb: float | None = 0.5
    #         ):
        
    #     def worker(rcv):
    #         rcv.estimate_expected_returns(
    #             estimation_method=estimation_method,
    #             bandwidth_method=bandwidth_method,
    #             bandwidth_value=bandwidth_value,
    #             lmb=lmb
    #         )

    #         print("estimado")
        
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #         futures = [executor.submit(worker, rcv) for rcv in self.models]

    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
    #     self._expected_returns = None

    def estimate_expected_returns(
            self, 
            estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
            bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
            bandwidth_value : int | None = 10, 
            lmb: float | None = 0.5
            ):
        
        for rcv in self.models:
            rcv.estimate_expected_returns(
                estimation_method=estimation_method,
                bandwidth_method=bandwidth_method,
                bandwidth_value=bandwidth_value,
                lmb=lmb
            )
        
        self._expected_returns = None

    # def estimate_expected_returns(
    #         self, 
    #         estimation_method : SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod = SimpleReturnsCovarianceModel.ExpectedReturnEstimationMethod.SIMPLE, 
    #         bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
    #         bandwidth_value : int | None = 10, 
    #         lmb: float | None = 0.5
    #         ):
        
    #     def process(rcv):
    #         print(f"[START] {threading.current_thread().name} -> {rcv}")
    
    #         rcv.estimate_expected_returns(
    #             estimation_method=estimation_method,
    #             bandwidth_method=bandwidth_method,
    #             bandwidth_value=bandwidth_value,
    #             lmb=lmb
    #         )
            
    #         print(f"[END]   {threading.current_thread().name} -> {rcv}")

    #     threads = []

    #     for i, rcv in enumerate(self.models):
    #         t = threading.Thread(
    #             target=process, 
    #             args=(rcv,),
    #             name=f"Worker-{i}"
    #         )
    #         threads.append(t)

    #     for t in threads:
    #         t.start()

    #     for t in threads:
    #         t.join()
        
    #     self._expected_returns = None

    @property
    def covariance_matrix(self) -> pd.DataFrame:
        return self.covariance_matrix_stats['mean']

    # def estimate_covariance_matrix(
    #         self, 
    #         covariance_method : SimpleReturnsCovarianceModel.CovarianceMethod = SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE, 
    #         bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
    #         bandwidth_value: int | None = 10, 
    #         weighting_method: SimpleReturnsCovarianceModel.WeightingMethod | None = SimpleReturnsCovarianceModel.WeightingMethod.CONSTANT, 
    #         lmb: float | None = 0.5
    #         ):

    #     def worker(rcv):
    #         rcv.estimate_covariance_matrix(
    #             covariance_method = covariance_method,
    #             bandwidth_method = bandwidth_method,
    #             bandwidth_value = bandwidth_value,
    #             weighting_method = weighting_method, 
    #             lmb = lmb
    #         )
        
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #         futures = [executor.submit(worker, rcv) for rcv in self.models]

    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]


    #     self._covariance_matrix = None
    #     self._correlation_matrix = None

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

    # def estimate_covariance_matrix(
    #         self, 
    #         covariance_method : SimpleReturnsCovarianceModel.CovarianceMethod = SimpleReturnsCovarianceModel.CovarianceMethod.SIMPLE, 
    #         bandwidth_method: SimpleReturnsCovarianceModel.BandwidthMethod | None = SimpleReturnsCovarianceModel.BandwidthMethod.NEWEY_WEST_RULE_OF_THUMB, 
    #         bandwidth_value: int | None = 10, 
    #         weighting_method: SimpleReturnsCovarianceModel.WeightingMethod | None = SimpleReturnsCovarianceModel.WeightingMethod.CONSTANT, 
    #         lmb: float | None = 0.5
    #         ):

    #     def process(rcv):
    #         rcv.estimate_covariance_matrix(
    #             covariance_method = covariance_method,
    #             bandwidth_method = bandwidth_method,
    #             bandwidth_value = bandwidth_value,
    #             weighting_method = weighting_method, 
    #             lmb = lmb
    #         )

    #     threads = []

    #     for rcv in self.models:
    #         t = threading.Thread(target=process, args=(rcv,))
    #         threads.append(t)

    #     for t in threads:
    #         t.start()

    #     for t in threads:
    #         t.join()

    #     self._covariance_matrix = None
    #     self._correlation_matrix = None


    @property
    def correlation_matrix(self) -> pd.DataFrame:
        return self.correlation_matrix_stats['mean']