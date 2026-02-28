
import streamlit as st
import pandas as pd
from services.MarketData_V2 import MarketData_V2
from pathlib import Path
from pages.utils.main_utils import *

def validate_import_df(market_data, df):
    valid = True
    no_ticker_rows = df[df["ticker"].isna() | (df["ticker"].str.strip() == "")]

    if not no_ticker_rows.empty:
        st.error(f"¡Error! You must especify a ticker in rows: {no_ticker_rows.index.tolist()}")
        valid = False

    for ticker in df["ticker"]:
        if not market_data.valid_ticker(ticker):
            st.error(f"¡Error! {ticker} is not a valid ticker")
            valid = False

    return valid

def equal_imports(market_data, df):
    if set(market_data.imported_assets_metadata.index) != set(df.ticker):
        return False
    
    for asset in df.itertuples():
        if market_data.imported_assets_metadata.loc[asset.ticker].asset_name != asset.asset_name:
            return False
        
    return True

def default_market_data():
    #path = 'C:/Users/alons/Desktop/Gestión cartera/Valores liquidativos fondos/V2'

    #asset_universe = pd.read_excel(path + '/asset_universe.xlsx', index_col='asset')

    # asset_universe = pd.DataFrame()

    # asset_universe.index.name = 'asset'

    # asset_universe.index = [
    #     'ES0112611001',
    #     'ES0159259011',
    #     'LU1598719752',
    #     'LU1598720172',
    #     'LU3038481936',
    #     'IE00BYX5NX33',
    #     'IE0031786696',
    #     'IE0032620787',
    #     'IE00B42LF923',
    #     'IE00BD0NCM55',
    #     'IE00BYX5MX67',
    #     'IE00B42W3S00',
    #     'ES0165265002'
    # ]

    # asset_universe['source'] = [
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local',
    #     'local'
    # ]

    # asset_universe['file'] = [
    #     'ES0112611001.json',
    #     'ES0159259011.json',
    #     'LU1598719752.json',
    #     'LU1598720172.json',
    #     'LU3038481936.json',
    #     'IE00BYX5NX33.json',
    #     'IE0031786696.json',
    #     'IE0032620787.json',
    #     'IE00B42LF923.json',
    #     'IE00BD0NCM55.json',
    #     'IE00BYX5MX67.json',
    #     'IE00B42W3S00.json',
    #     'ES0165265002.json'
    # ]

    # asset_universe['asset_name'] = [
    #     'Azvalor Internacional FI',
    #     'Magallanes European Equity M FI',
    #     'Cobas International Fund-P Acc EUR',
    #     'Cobas Large Cap Fund-P Acc EUR',
    #     'Hamco SICAV - Global Value R EUR Acc',
    #     'Fidelity MSCI World Index Fund P-ACC-EUR',
    #     'Vanguard Emerging Markets Stock Index Fund EUR Acc',
    #     'Vanguard U.S. 500 Stock Index Fund Investor EUR Accumulation',
    #     'Vanguard Global Small-Cap Index Fund USD Acc',
    #     'iShares Developed World Index (IE) D Acc EUR',
    #     'Fidelity S&P 500 Index Fund P-ACC-EUR',
    #     'Vanguard Global Small-Cap Index Fund Investor EUR Accumulation',
    #     'MyInvestor Nasdaq 100'
    # ]

    # asset_universe['America'] = [
    #     0.5334,
    #     0.0631,
    #     0.1586,
    #     0.1586,
    #     0.2163,
    #     0.7503,
    #     0.0766,
    #     0.9947,
    #     0.6469,
    #     0.7591,
    #     0.9947,
    #     0.6469,
    #     0.9798
    # ]

    # asset_universe['Europe'] = [
    #     0.4194,
    #     0.9369,
    #     0.6626,
    #     0.6626,
    #     0.1793,
    #     0.1651,
    #     0.1209,
    #     0.0041,
    #     0.1733,
    #     0.1595,
    #     0.0041,
    #     0.1733,
    #     0.0160
    # ]

    # asset_universe['Asia'] = [
    #     0.0473,
    #     0.0000,
    #     0.1788,
    #     0.1788,
    #     0.6045,
    #     0.0846,
    #     0.8026,
    #     0.0011,
    #     0.1798,
    #     0.0813,
    #     0.0011,
    #     0.1798,
    #     0.0042
    # ]

    # print(asset_universe)
    # print(asset_universe_2)

    #return MarketData_V2(asset_universe, path)

    path = read_key('data_path')

    return MarketData_V2(path)

def asset_import_df(market_data):
    df = pd.DataFrame(columns=['ticker', 'asset_name'])

    if not market_data.imported_assets_metadata.empty:
        tmp_df = market_data.imported_assets_metadata.copy()
        tmp_df['ticker'] = tmp_df.index
        df = tmp_df[['ticker', 'asset_name']].reset_index(drop=True)

    return df