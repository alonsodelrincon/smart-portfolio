from abc import ABC, abstractmethod

class DataProvider(ABC):
    @property
    @abstractmethod
    def returns_len(self):
        pass
    
    @property
    @abstractmethod
    def n_assets(self):
        pass
    
    @property
    @abstractmethod
    def assets(self):
        pass
    
    @property
    @abstractmethod
    def returns(self):
        pass

    @abstractmethod
    def asset_name(self, asset: str):
        pass
