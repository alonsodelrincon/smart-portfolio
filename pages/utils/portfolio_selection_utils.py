import streamlit as st
import pandas as pd
from services.MarketData_V2 import MarketData_V2
from services.ReturnsCovarianceModel import ReturnsCovarianceModel

from pages.utils.main_utils import *

def default_market_data():
    return MarketData_V2(db_path())

def default_covariance_model(market_data):
    return ReturnsCovarianceModel(market_data=market_data)

def load_covariance_model_returns(covariance_model):
    return_bandwidth_value = get_config()['return_bandwidth_value']

    if return_bandwidth_value is not None and return_bandwidth_value >= covariance_model.market_data.returns_len - 1:
        return_bandwidth_value = covariance_model.market_data.returns_len - 2

    covariance_model.estimate_expected_returns(
        estimation_method = get_config()['return_estimation_method'],
        bandwidth_method = get_config()['return_bandwidth_method'],
        bandwidth_value = get_config()['return_bandwidth_value'],
        lmb = get_config()['return_lmb'],
    )
    

def load_covariance_model_covariance(covariance_model):
    covariance_bandwidth_value = get_config()['covariance_bandwidth_value']

    if covariance_bandwidth_value is not None and covariance_bandwidth_value >= covariance_model.market_data.returns_len - 1:
        covariance_bandwidth_value = covariance_model.market_data.returns_len - 2

    covariance_model.estimate_covariance_matrix(
        covariance_method = get_config()['covariance_estimation_method'],
        bandwidth_method = get_config()['covariance_bandwidth_method'],
        bandwidth_value = covariance_bandwidth_value,
        weighting_method = ReturnsCovarianceModel.WeightingMethod.BARLETT, 
        lmb = None
    )

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

def asset_import_df(market_data):
    df = pd.DataFrame(columns=['ticker', 'asset_name'])

    if not market_data.imported_assets_metadata.empty:
        tmp_df = market_data.imported_assets_metadata.copy()
        tmp_df['ticker'] = tmp_df.index
        df = tmp_df[['ticker', 'asset_name']].reset_index(drop=True)

    return df