from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status

from models import InvestmentRequestData
from .utils import summary_risk_indicator, performance_scenarios, transaction_costs, reduction_in_yield, cost_over_time, ongoing_charges, one_off_costs, incidental_costs
import pandas as pd
import os

router = APIRouter()
load_dotenv()

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# can use org uuid as apikey, or hashed uuid
API_KEYS = os.environ.get("API_KEYS", "").split(",")
API_KEY_NAME = os.environ.get("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key in API_KEYS:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@router.get("/", status_code=status.HTTP_200_OK)
async def check():
    return {"Hello": "User"}

@router.post("/calculate", status_code=status.HTTP_201_CREATED)
async def calculate(data: InvestmentRequestData, api_key: str = Depends(get_api_key)):
    ## Following code will be replaced with actual implementation
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Load historical price data
    historical_prices_file_path = os.path.join(base_path, 'sample_data', 'historical_price_data.csv')
    historical_prices = pd.read_csv(historical_prices_file_path)
    # Load transaction data
    transaction_data_file_path = os.path.join(base_path, 'sample_data', 'transaction_data.csv')
    transaction_data = pd.read_csv(transaction_data_file_path)
    
    # settings
    investment_amount = data.investment_amount
    investment_period = data.investment_period
    management_fee_percentage = data.management_fee_percentage
    other_ongoing_costs_percentage = data.other_ongoing_costs_percentage
    entry_cost_percentage = data.entry_cost_percentage
    exit_cost_percentage = data.exit_cost_percentage
    performance_fee_percentage = data.performance_fee_percentage
    benchmark_return = data.benchmark_return
    actual_return = data.actual_return
    
    summary_risk_indicator_result = summary_risk_indicator(historical_prices)
    performance_scenarios_result = performance_scenarios(historical_prices, investment_amount, investment_period)
    performance_scenarios_one_year_result = performance_scenarios(historical_prices, investment_amount, 1)
    transaction_costs_result = transaction_costs(transaction_data, investment_amount)
    reduction_in_yield_result = reduction_in_yield(management_fee_percentage, transaction_costs_result["transactionCostPercentage"], investment_period)
    cost_over_time_result = cost_over_time(investment_amount, management_fee_percentage, transaction_costs_result["transactionCostPercentage"], investment_period)
    ongoing_charges_result = ongoing_charges(management_fee_percentage, other_ongoing_costs_percentage)
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

@router.get("/test", status_code=status.HTTP_200_OK)
async def test():
    response = supabase.table("test").select("*").execute()
    return response