
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
    return MarketData_V2(db_path())

def asset_import_df(market_data):
    df = pd.DataFrame(columns=['ticker', 'asset_name'])

    if not market_data.imported_assets_metadata.empty:
        tmp_df = market_data.imported_assets_metadata.copy()
        tmp_df['ticker'] = tmp_df.index
        df = tmp_df[['ticker', 'asset_name']].reset_index(drop=True)

    return df