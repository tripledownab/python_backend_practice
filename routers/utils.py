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
    return {"stressScenario": round(stress_scenario, 2), "unfavorableScenario": round(unfavorable_scenario, 2), 
            "moderateScenario": round(moderate_scenario, 2), "favorableScenario": round(favorable_scenario, 2)}
    
def transaction_costs(transaction_data, investment_amount: int):
    transaction_data['Slippage'] = (transaction_data['Execution Price'] - transaction_data['Arrival Price']) * transaction_data['Units Traded']
    total_slippage = transaction_data['Slippage'].sum()
    total_trade_amount = (transaction_data['Execution Price'] * transaction_data['Units Traded']).sum()
    transaction_cost_percentage = (total_slippage / total_trade_amount) * 100
    transaction_cost_currency = (transaction_cost_percentage / 100) * investment_amount
    return {"transactionCostPercentage":round(transaction_cost_percentage, 4), "transactionCostInCurrency":round(transaction_cost_currency, 2)}

def reduction_in_yield(management_fee_percentage: float, transaction_cost_percentage: float, investment_period: int) -> float:
    riy_1_year = (management_fee_percentage + transaction_cost_percentage) * 1 
    riy_rhp = (management_fee_percentage + transaction_cost_percentage) * investment_period
    return {"riy_1_year": round(riy_1_year, 2), "riy_rhp": round(riy_rhp, 2)}

def cost_over_time(initial_investment, management_fee_percentage, transaction_cost_percentage, investment_period):
    annual_cost_percentage = management_fee_percentage + transaction_cost_percentage
    costs_one_year = initial_investment * (annual_cost_percentage / 100)
    costs_suggested_period = initial_investment * ((1 + (annual_cost_percentage / 100)) ** investment_period - 1)
    return {"costsOneYear": round(costs_one_year, 2), "costsSuggestedPeriod": round(costs_suggested_period, 2)}

def ongoing_charges(annual_management_fee: float, other_ongoing_costs: float) -> float:
    total_ongoing_charges = annual_management_fee + other_ongoing_costs
    return total_ongoing_charges

def one_off_costs(entry_cost_percentage, exit_cost_percentage, initial_investment):
    entry_costs = initial_investment * (entry_cost_percentage / 100)
    exit_costs = initial_investment * (exit_cost_percentage / 100)
    return {"entryCosts": entry_costs, "exitCosts": exit_costs}

def incidental_costs(performance_fee_percentage: float, benchmark_return: float, actual_return: float, initial_investment: int) -> float:
    if actual_return > benchmark_return:
        performance_fee = initial_investment * ((actual_return - benchmark_return) * (performance_fee_percentage / 100))
    else:
        performance_fee = 0.0
    return round(performance_fee, 2)