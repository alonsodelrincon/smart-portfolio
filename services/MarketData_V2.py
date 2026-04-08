import pandas as pd
import numpy as np
import numpy as np
import yfinance as yf
from pathlib import Path

class MarketData_V2:
    def __init__(self, local_dir: Path):
        self._local_dir = local_dir
        
        self._local_assets_metadata = pd.read_excel(local_dir / 'asset_universe.xlsx', index_col='asset')

        self._validate_local_metadata()

        self._selected_assets = []

        self._imported_assets_metadata = pd.DataFrame(columns=['source','file','asset_name','America','Europe','Asia', 'marketCap', 'currency'])

        self._local_assets_df = pd.DataFrame()
        self._imported_assets_df_cache = pd.DataFrame()
        
        self._total_returns_df = None
        self._returns_df = None

        self._load_universe()

    def _validate_local_metadata(self):
        if set(self._local_assets_metadata.columns) != set(['source','file','asset_name','America','Europe','Asia']):
            raise ValueError(f"Asset metadata is not valid")

    def _load_universe(self):
        complete_df_tmp = []

        for asset in self._local_assets_metadata.itertuples():
            df = self._read_local_asset(asset=asset.Index, file=asset.file)
            complete_df_tmp.append(df)

        self._local_assets_df = pd.concat(complete_df_tmp)

    def _read_local_asset(self, asset:str, file: str):
        path = self._local_dir / file

        try:
            df_tmp = pd.read_json(path).explode("series")
        except FileNotFoundError:
            raise FileNotFoundError(f"File doesn't exist: {path}")
        except ValueError as e:
            raise ValueError(f"Error reading JSON from {path}: {e}")

        df = pd.json_normalize(df_tmp["series"])
        df['asset'] = asset
        df.date = pd.to_datetime(df.date)
        df = df.set_index(['asset', 'date'])

        return df
    
    @property
    def _selected_assets_df(self):
        return self._local_assets_df.loc[self._selected_assets]

    @property
    def _imported_assets_df(self):
        if set(self._imported_assets_df_cache.index.get_level_values(0)) != set(self._imported_assets_metadata.index):
            ticker_assets_df_t = []

            for asset in self._imported_assets_metadata.itertuples():
                df = self._load_ticker_asset(ticker=asset.Index)
                ticker_assets_df_t.append(df)

            self._imported_assets_df_cache = pd.concat(ticker_assets_df_t)
        
        return self._imported_assets_df_cache

    def _load_ticker_asset(self, ticker: str, start: str='2001-01-01'):
        asset_data = yf.Ticker(ticker)

        if asset_data.info.get("regularMarketPrice") is None:
            raise ValueError(f"The ticker {ticker} cant be found")
            
        asset_prices = asset_data.history(start = start, auto_adjust=False)

        if asset_prices.empty:
            raise ValueError(f"No data returned for ticker {ticker} starting from {start}")

        asset_prices.index = asset_prices.index.tz_localize(None)

        df = pd.DataFrame({
            'asset': ticker,
            'nav': asset_prices['Close'],
            'totalReturn': asset_prices['Adj Close']
        }, index=asset_prices.index)

        df.index.name = 'date'
        df = df.reset_index().set_index(['asset', 'date'])

        return df

    @property
    def valid(self):
        return len(self.active_assets) >= 2

    @property
    def local_assets(self):
        return self._local_assets_metadata[['asset_name']]
    
    @property
    def selected_assets(self):
        return self._local_assets_metadata[['asset_name']].loc[self._selected_assets]
    
    @property
    def local_assets_metadata(self):
        return self._local_assets_metadata
    
    @property
    def selected_assets_metadata(self):
        return self._local_assets_metadata.loc[self._selected_assets]
    
    @property
    def imported_assets(self):
        return self._imported_assets_metadata[['asset_name']]

    @property
    def imported_assets_metadata(self):
        return self._imported_assets_metadata

    @property
    def active_assets(self):
        return pd.concat([self.selected_assets, self.imported_assets]) 
    
    @property
    def active_assets_metadata(self):
        return pd.concat([self.imported_assets_metadata, self.selected_assets_metadata])


    def select_assets(self, assets: list[str]) -> None:
        invalid = set(assets) - set(self._local_assets_metadata.index)
        if invalid:
            raise ValueError(f"Invalid assets: {invalid}")

        self._selected_assets = assets
        self._reset_dates()

    def import_asset(self, ticker: str, name: str, diversification: dict | None = None) -> None:
        if not self.valid_ticker(ticker):
            raise ValueError(f"The ticker {ticker} cant be found")

        if ticker in set(self._imported_assets_metadata.index):
            raise ValueError(f"The ticker {ticker} is already imported")

        diversification = diversification or {}

        ticker_data = yf.Ticker(ticker)

        ticker_info = {
            'source': 'yf',
            'asset_name': name,
            'America': diversification.get('America'),
            'Europe': diversification.get('Europe'),
            'Asia': diversification.get('Asia'),
            'marketCap': ticker_data.info.get("marketCap"),
            'currency': ticker_data.info['currency']
        }

        self._imported_assets_metadata.loc[ticker] = ticker_info
        self._reset_dates()

    def reset_imported_assets(self):
        self._imported_assets_metadata = pd.DataFrame(columns=['source','file','asset_name','America','Europe','Asia', 'marketCap', 'currency'])
        self._imported_assets_df_cache = pd.DataFrame()

    def _reset_dates(self):
        self._from_date = None
        self._to_date = None
        self._reset_returns()

    def _reset_returns(self):
        self._total_returns_df = None
        self._returns_df = None

    def valid_ticker(self, ticker: str) -> bool:
        asset_data = yf.Ticker(ticker)

        if asset_data.info.get("regularMarketPrice") is None:
            return False
        
        return True

    def delete_imported_asset(self, ticker:str) -> None:
        if ticker not in set(self._imported_assets_metadata.index):
            raise ValueError(f"The ticker {ticker} does not exist")
        
        self._imported_assets_metadata.drop(ticker, inplace=True)

    @property
    def first_date(self):
        '''
        selected_first_date = np.max(self._selected_assets_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").min()))
        
        imported_first_date = np.max(self._imported_assets_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").min()))

        return np.max(selected_first_date, imported_first_date)
        '''
        dfs = [self._selected_assets_df, self._imported_assets_df]
        total_df = pd.concat([d for d in dfs if not d.empty])

        if total_df.empty:
            raise ValueError("At least one asset must be selected")

        return total_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").min()).max()
        
    @property
    def last_date(self):
        '''
        selected_first_date = np.min(self._selected_assets_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").max()))
        
        imported_first_date = np.min(self._imported_assets_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").max()))

        return np.min(selected_first_date, imported_first_date)
        '''
        dfs = [self._selected_assets_df, self._imported_assets_df]
        total_df = pd.concat([d for d in dfs if not d.empty])

        if total_df.empty:
            raise ValueError("At least one asset must be selected")

        return total_df.groupby(level="asset").apply(lambda x: x.index.get_level_values("date").max()).min()

    @property
    def from_date(self):
        if self._from_date is None:
            return self.first_date

        return self._from_date
    
    @property
    def to_date(self):
        if self._to_date is None:
            return self.last_date
        
        return self._to_date

    @from_date.setter
    def from_date(self, value: pd.Timestamp | None = None) -> None:
        if value is None or (self.first_date <= value and value <= self.last_date):
            self._from_date = value
            self._reset_returns()
        else:
            raise ValueError(f"The from date muyst be between {self.first_date} and {self.last_date}")

    @to_date.setter
    def to_date(self, value: pd.Timestamp | None = None) -> None:
        if value is None or (self.first_date <= value and value <= self.last_date):
            self._to_date = value
            self._reset_returns()
        else:
            raise ValueError(f"The to date muyst be between {self.first_date} and {self.last_date}")

    @property
    def total_returns_df(self):
        if self._total_returns_df is not None:
            return self._total_returns_df

        df_tmp = pd.concat([self._selected_assets_df, self._imported_assets_df])
        
        if self.from_date != None:
            df_tmp = df_tmp[df_tmp.index.get_level_values('date') > self.from_date]
        else:
            df_tmp = df_tmp[df_tmp.index.get_level_values('date') > self.first_date]
            
        if self.to_date != None:
            df_tmp = df_tmp[df_tmp.index.get_level_values('date') < self.to_date]
        else:
            df_tmp = df_tmp[df_tmp.index.get_level_values('date') < self.last_date]

        if len(df_tmp) == 0:
            raise ValueError(f"The dataframe has not enough returns for selected from and to dates")
        
        self._total_returns_df = df_tmp
        return  self._total_returns_df
    
    @property
    def returns_df(self):
        if self._returns_df is not None:
            return self._returns_df
        
        df_pivot = self.total_returns_df['totalReturn'].unstack(level=0)
        df_pivot.sort_index(inplace=True)
        df_pivot.columns.name = 'totalReturn'
        df_pivot.dropna(inplace=True)

        if l := len(df_pivot) < 2:
            raise ValueError(f"The dataframe has not enough matching returns (i.e returns in the same date) found {l}")
        
        self._returns_df = df_pivot.pct_change().dropna()
        return self._returns_df
    
    @property
    def returns_len(self):
        return len(self.returns_df)
    
    @property
    def n_active_assets(self):
        return len(self.active_assets)
    
    def asset_name(self, asset: str):
        return self.active_assets.loc[asset].asset_name

    
    def _currency_exchange(self, from_currency: str, to_currency: str):
        exchange_map = pd.DataFrame()

        exchange_map = pd.DataFrame(index=[
            'EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X',
            'EURGBP=X', 'EURJPY=X', 'GBPJPY=X', 'EURCAD=X',
            'EURSEK=X', 'EURCHF=X', 'EURHUF=X', 'USDJPY=X',
            'USDCHF=X', 'USDCNY=X', 'USDZAR=X', 'USDINR=X',
            'USDSGD=X', 'USDMXN=X', 'USDPHP=X', 'USDTHB=X',
            'USDIDR=X'
        ])

        exchange_map['from'] = [
            'EUR', 'GBP', 'AUD', 'NZD', 'EUR', 'EUR', 'GBP', 'EUR',
            'EUR', 'EUR', 'EUR', 'USD', 'USD', 'USD', 'USD', 'USD',
            'USD', 'USD', 'USD', 'USD', 'USD'
        ]

        exchange_map['to'] = [
            'USD', 'USD', 'USD', 'USD', 'GBP', 'JPY', 'JPY', 'CAD',
            'SEK', 'CHF', 'HUF', 'JPY', 'CHF', 'CNY', 'ZAR', 'INR',
            'SGD', 'MXN', 'PHP', 'THB', 'IDR'
        ]

        exchange_ticker = None
        inverted_exchange = False

        if ((exchange_map['from'] == from_currency) & (exchange_map['to'] == to_currency)).any():
            exchange_ticker = exchange_map[(exchange_map['from'] == from_currency) & (exchange_map['to'] == to_currency)].index[0]

        if ((exchange_map['to'] == from_currency) & (exchange_map['from'] == to_currency)).any():
            exchange_ticker = exchange_map[(exchange_map['to'] == from_currency) & (exchange_map['from'] == to_currency)].index[0]
            inverted_exchange = True
        
        exchange_data = yf.Ticker(exchange_ticker).history(start="1900-01-01", auto_adjust=False)

        exchange_df = pd.DataFrame({
            'exchange_rate': exchange_data['Close']
        }, index=exchange_data.index)

        exchange_df.index.name = 'date'

        if inverted_exchange:
            exchange_df['exchange_rate'] = 1/exchange_df['exchange_rate']

        if exchange_df.empty:
            raise ValueError(f"No data returned for exchange {exchange_ticker}")

        exchange_df.index = exchange_df.index.tz_localize(None)

        exchange_df = exchange_df.asfreq('D')
        exchange_df = exchange_df.ffill()
        exchange_df = exchange_df.bfill()
        
        return exchange_df


