import numpy as np
import pandas as pd

def SummaryRiskIndicator(historical_prices: pd.DataFrame) -> int:
    # Calculate daily returns
    # NOTE: some data has returns already calculated
    historical_prices['Return'] = historical_prices['Price (€)'].pct_change()
    
    # Calculate annualized volatility
    daily_volatility = np.std(historical_prices['Return'].dropna())
    annualized_volatility = daily_volatility * np.sqrt(252)  # Assuming 252 trading days
    
    # Determine the risk class based on volatility
    risk_class = None
    if annualized_volatility < 0.005:
        risk_class = 1
    elif annualized_volatility < 0.12:
        risk_class = 2
    elif annualized_volatility < 0.20:
        risk_class = 3
    elif annualized_volatility < 0.30:
        risk_class = 4
    elif annualized_volatility < 0.40:
        risk_class = 5
    elif annualized_volatility < 0.50:
        risk_class = 6
    else:
        risk_class = 7
        
    print(risk_class)
    return risk_class