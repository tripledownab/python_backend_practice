from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic_settings import BaseSettings, SettingsConfigDict
    
class InvestmentRequestData(BaseModel):
    investment_amount: float
    investment_period: int
    management_fee_percentage: float
    other_ongoing_costs: float
    entry_cost_percentage: float
    exit_cost_percentage: float
    performance_fee_percentage: float
    benchmark_return: float
    actual_return: float
    
    model_config = {
        "json_schema_extra": {
            "example": {
            "investment_amount": 100000,
            "investment_period": 3,
            "management_fee_percentage": 1.0,
            "other_ongoing_costs": 0.3,
            "entry_cost_percentage": 0.5,
            "exit_cost_percentage": 0.5,
            "performance_fee_percentage": 20.0,
            "benchmark_return": 0.05,
            "actual_return": 0.10
            }
        }
        }

class User (BaseModel):
    id: int
    username: str
    password: str # should be hashed
    