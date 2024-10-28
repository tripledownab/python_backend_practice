from fastapi import APIRouter
from starlette import status
from .utils import summary_risk_indicator, performance_scenarios, transaction_costs, reduction_in_yield, cost_over_time, ongoing_charges, one_off_costs, incidental_costs
import pandas as pd
import os

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def check():
    return {"Hello": "World"}

@router.post("/calculate", status_code=status.HTTP_201_CREATED)
async def calculate():
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Load historical price data
    historical_prices_file_path = os.path.join(base_path, 'sample_data', 'historical_price_data.csv')
    historical_prices = pd.read_csv(historical_prices_file_path)
    # Load transaction data
    transaction_data_file_path = os.path.join(base_path, 'sample_data', 'transaction_data.csv')
    transaction_data = pd.read_csv(transaction_data_file_path)
    
    # settings
    investment_amount=100000
    investment_period=3
    management_fee_percentage = 1.0  
    other_ongoing_costs = 0.3
    entry_cost_percentage = 0.5
    exit_cost_percentage = 0.5
    performance_fee_percentage = 20.0  
    benchmark_return = 0.05  
    actual_return = 0.10 
    
    summary_risk_indicator_result = summary_risk_indicator(historical_prices)
    performance_scenarios_result = performance_scenarios(historical_prices, investment_amount, investment_period)
    performance_scenarios_one_year_result = performance_scenarios(historical_prices, investment_amount, 1)
    transaction_costs_result = transaction_costs(transaction_data, investment_amount)
    reduction_in_yield_result = reduction_in_yield(management_fee_percentage, transaction_costs_result["transactionCostPercentage"], investment_period)
    cost_over_time_result = cost_over_time(investment_amount, management_fee_percentage, transaction_costs_result["transactionCostPercentage"])
    ongoing_charges_result = ongoing_charges(management_fee_percentage, other_ongoing_costs)
    one_off_costs_result = one_off_costs(entry_cost_percentage, exit_cost_percentage, investment_amount)
    incidental_costs_result = incidental_costs(performance_fee_percentage, benchmark_return, actual_return, investment_amount)
    
    return {"summaryRiskIndicator": summary_risk_indicator_result, 
            "performanceScenariosOneYear": performance_scenarios_one_year_result, 
            "performanceScenariosSuggestedPeriod": performance_scenarios_result, 
            "transactionCosts": transaction_costs_result,
            "reductionInYield":reduction_in_yield_result,
            "costOverTime": cost_over_time_result,
            "ongoingCharges": ongoing_charges_result,
            "oneOffCosts": one_off_costs_result,
            "incidentalCosts": incidental_costs_result}

