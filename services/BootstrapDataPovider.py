from services.DataProvider import DataProvider
from services.SampleDataProvider import SampleDataProvider

class BlockBootstrapDataProvider(DataProvider):
    def __init__(self, data_provider: DataProvider, bootstrap_length = 100, block_length = 30):
        self._data_provider = data_provider

        self._bootstrap_samples = [SampleDataProvider(data_provider=data_provider, block_length=block_length) for _ in range(bootstrap_length)]

        self._returns = None
        self._block_length = block_length

    @property
    def data_provider(self):
        return self._data_provider

    @property
    def returns_len(self):
        return self.data_provider.returns_len
    
    @property
    def n_assets(self):
        return self.data_provider.n_assets
    
    @property
    def assets(self):
        return self.data_provider.assets
    
    @property
    def block_length(self):
        return self._block_length
    
    @property
    def returns(self):
        return self._bootstrap_samples[0].returns
    
    @property
    def all_returns(self):
        return [b_s.returns for b_s in self._bootstrap_samples]

    @property
    def bootsrtap_samples(self):
        return self._bootstrap_samples

    def asset_name(self, asset: str):
        return self.data_provider.asset_name(asset)

