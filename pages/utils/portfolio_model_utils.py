from services.PortfolioOptimizerModel import PortfolioOptimizerModel

def default_portfolio_model(returns_covariance_model):
    return PortfolioOptimizerModel(returns_covariance_model=returns_covariance_model)

def default_portfolio_steps():
    return 20