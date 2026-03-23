from services.DataProvider import DataProvider
from services.MarketData_V2 import MarketData_V2

class MarketDataProvider(DataProvider):
    def __init__(self, market_data: MarketData_V2):
        self._market_data = market_data

    @property
    def returns_len(self):
        return self._market_data.returns_len
    
    @property
    def n_assets(self):
        return self._market_data.n_active_assets
    
    @property
    def assets(self):
        return self._market_data.active_assets
    
    @property
    def returns(self):
        return self._market_data.returns_df

    def asset_name(self, asset: str):
        return self._market_data.asset_name(asset)