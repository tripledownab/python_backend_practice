from fastapi import APIRouter
from starlette import status
from .utils import SummaryRiskIndicator
import pandas as pd
import os

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def check():
    return {"Hello": "World"}

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create():
    # Load historical price data
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'sample_data', 'historical_price_data.csv')
    historical_prices = pd.read_csv(file_path)
    
    summary_risk_indicator = SummaryRiskIndicator(historical_prices)
    
    return {"Summary Risk Indicator": summary_risk_indicator}

