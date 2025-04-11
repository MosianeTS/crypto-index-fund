from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Crypto Index Fund API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Asset(BaseModel):
    symbol: str
    market_cap: float = Field(gt=0)
    price: float = Field(gt=0)

class FundParameters(BaseModel):
    asset_cap: float = Field(gt=0, le=1.0)
    total_capital: float = Field(gt=0)
    assets: List[Asset]

class AssetAllocation(BaseModel):
    symbol: str
    amount: float
    percentage: float
    capital_allocation: float
   

class FundAllocation(BaseModel):
    allocations: List[AssetAllocation]

def calculate_allocations(assets, asset_cap, total_capital):
    """
    Calculate allocations for a crypto index fund with an asset cap.
    
    Parameters:
    - assets: List of Asset objects containing symbol, market_cap, and price
    - asset_cap: Maximum percentage allocation for any single asset (0.0 to 1.0)
    - total_capital: Total capital to allocate (in ZAR)
    
    Returns:
    - List of allocation details for each asset
    """
    assets_dict = [{"symbol": asset.symbol, "market_cap": asset.market_cap, "price": asset.price} for asset in assets]    
    
    total_market_cap = sum(asset['market_cap'] for asset in assets_dict)
    
    if total_market_cap <= 0:
        raise HTTPException(status_code=400, detail="Total market cap must be greater than zero")
    
    # Calculate initial allocation percentages based on market cap
    for asset in assets_dict:
        asset['initial_percentage'] = asset['market_cap'] / total_market_cap
    
    # Apply asset cap and redistribute excess
    excess = 0
    uncapped_market_cap = 0
    
    for asset in assets_dict:
        if asset['initial_percentage'] > asset_cap:
            excess += asset['initial_percentage'] - asset_cap
            asset['final_percentage'] = asset_cap
        else:
            asset['final_percentage'] = asset['initial_percentage']
            uncapped_market_cap += asset['market_cap']
    
    # Redistribute excess to uncapped assets proportionally
    if excess > 0 and uncapped_market_cap > 0:
        iterations = 0
        max_iterations = 100  
        
        while excess > 0.0001 and iterations < max_iterations:
            remaining_excess = 0
            current_excess = excess
            excess = 0
            
            for asset in assets_dict:
                if asset['final_percentage'] < asset_cap:
                   
                    if uncapped_market_cap > 0:
                        proportion = asset['market_cap'] / uncapped_market_cap
                      
                        additional = current_excess * proportion
                        asset['final_percentage'] += additional                        
         
                        if asset['final_percentage'] > asset_cap:
                            excess += asset['final_percentage'] - asset_cap
                            asset['final_percentage'] = asset_cap
                          
                            uncapped_market_cap -= asset['market_cap']
            
            iterations += 1    
   
    total_percentage = sum(asset['final_percentage'] for asset in assets_dict)    
   
    if abs(total_percentage - 1.0) > 0.0001:
        adjustment_factor = 1.0 / total_percentage
        for asset in assets_dict:
            asset['final_percentage'] *= adjustment_factor    
    
    for asset in assets_dict:
        asset['capital_allocation'] = asset['final_percentage'] * total_capital
        asset['amount'] = asset['capital_allocation'] / asset['price']
    
    # Format output
    allocations = []
    for asset in assets_dict:
        allocations.append({
            "symbol": asset["symbol"],         
            "percentage": asset["final_percentage"],
            "capital_allocation": asset["capital_allocation"],
            "amount": asset["amount"]
        })
    
    return allocations

@app.post("/calculate-fund", response_model=FundAllocation)
async def calculate_fund(parameters: FundParameters):
    try:
        allocations = calculate_allocations(
            parameters.assets,
            parameters.asset_cap,
            parameters.total_capital
        )
        return {"allocations": allocations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)