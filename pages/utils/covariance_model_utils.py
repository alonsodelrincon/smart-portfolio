from services.ReturnsCovarianceModel import ReturnsCovarianceModel

def default_covariance_model(market_data):
    return ReturnsCovarianceModel(market_data=market_data)

def default_bandwidth_value(market_data):
    return min(10, len(market_data.returns_df))