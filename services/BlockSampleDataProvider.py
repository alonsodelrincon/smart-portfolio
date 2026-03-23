from services.DataProvider import DataProvider
from services.MarketDataProvider import MarketDataProvider
import random 
import pandas as pd

class BlockSampleDataProvider(DataProvider):
    def __init__(self, data_provider: DataProvider,  block_length = 30):
        self._data_provider = data_provider

        self._random_state = random.randint(0,999999999)

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
        if self._returns is None:
            df_blocks = [self.data_provider.returns.iloc[i:i+self.block_length] for i in range(0, self.returns_len, self.block_length)]

            df_sample_blocks = [df.sample(n=len(df), random_state=self._random_state + i, replace=True) for (i, df) in enumerate(df_blocks)]

            self._returns = pd.concat(df_sample_blocks)

        return self._returns
    
    def asset_name(self, asset: str):
        return self.data_provider.asset_name(asset)

