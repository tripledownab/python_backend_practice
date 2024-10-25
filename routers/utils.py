import numpy as np
import pandas as pd

# formulated column head names
# Price, Return, Execution Price, Arrival Price, Units Traded, Slippage

def summary_risk_indicator(historical_prices: pd.DataFrame) -> int:
    # Calculate daily returns
    # NOTE: some data has returns already calculated
    historical_prices['Return'] = historical_prices['Price'].pct_change()
    
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

def performance_scenarios(historical_prices: pd.DataFrame, investment_amount: int, investment_period: int) -> dict:
    # Calculate percentiles for different scenarios
    worst_case = np.percentile(historical_prices['Return'].dropna(), 5)
    unfavorable_case = np.percentile(historical_prices['Return'].dropna(), 25)
    moderate_case = np.percentile(historical_prices['Return'].dropna(), 50)
    favorable_case = np.percentile(historical_prices['Return'].dropna(), 75)

    # Project future value based on annualized return for each scenario
    def project_value(investment, annual_return, years):
        return investment * (1 + annual_return) ** years

    # Calculate scenarios over a investment_period period
    stress_scenario = project_value(investment_amount, worst_case, investment_period)
    unfavorable_scenario = project_value(investment_amount, unfavorable_case, investment_period)
    moderate_scenario = project_value(investment_amount, moderate_case, investment_period)
    favorable_scenario = project_value(investment_amount, favorable_case, investment_period)

    print(f"Stress Scenario: {stress_scenario:.2f}")
    print(f"Unfavorable Scenario: {unfavorable_scenario:.2f}")
    print(f"Moderate Scenario: {moderate_scenario:.2f}")
    print(f"Favorable Scenario: {favorable_scenario:.2f}")
    
    return {"Stress Scenario": stress_scenario, "Unfavorable Scenario": unfavorable_scenario, 
            "Moderate Scenario": moderate_scenario, "Favorable Scenario": favorable_scenario}
    
def transaction_costs(transaction_data):
    # Calculate slippage for each transaction
    transaction_data['Slippage'] = (transaction_data['Execution Price'] - transaction_data['Arrival Price']) * transaction_data['Units Traded']

    # Calculate total transaction cost percentage
    total_slippage = transaction_data['Slippage'].sum()
    total_trade_amount = (transaction_data['Execution Price'] * transaction_data['Units Traded']).sum()
    transaction_cost_percentage = (total_slippage / total_trade_amount) * 100

    print(f"Total Transaction Cost Percentage: {transaction_cost_percentage:.2f}%")
    return transaction_cost_percentage