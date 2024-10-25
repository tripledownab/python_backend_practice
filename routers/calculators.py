from fastapi import APIRouter
from starlette import status
from .utils import summary_risk_indicator, performance_scenarios, transaction_costs
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
    
    summary_risk_indicator_result = summary_risk_indicator(historical_prices)
    performance_scenarios_result = performance_scenarios(historical_prices, investment_amount=10000, investment_period=3)
    transaction_costs_result = transaction_costs(transaction_data)
    
    return {"Summary Risk Indicator": summary_risk_indicator_result, 
            "Performance Scenarios": performance_scenarios_result, 
            "Transaction Costs": transaction_costs_result}

