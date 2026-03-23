from services.DataProvider import DataProvider
from services.MarketDataProvider import MarketDataProvider
import random 

class BootstrapDataProvider(DataProvider):
    def __init__(self, data_provider: MarketDataProvider):
        self._data_provider = data_provider

        self._random_state = random.randint(0,999999999)

        self._returns = None

    @property
    def data_provider(self):
        return self._data_provider

    @property
    def returns_len(self):
        return self._data_provider.returns_len
    
    @property
    def n_assets(self):
        return self._data_provider.n_assets
    
    @property
    def assets(self):
        return self._data_provider.assets
    
    @property
    def returns(self):
        if self._returns is None:
            self._returns = self.data_provider.returns.sample(n=self.returns_len, random_state=self._random_state, replace=True)

        return self._returns
    
    def asset_name(self, asset: str):
        return self.data_provider.asset_name(asset)

