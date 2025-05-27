from fastapi import FastAPI, Query
from alert import check_price_alert

app = FastAPI(
    title="Crypto Price Alert Server",
    description="Kripto para fiyat alarm sistemi",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy", "service": "crypto-price-alert"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Crypto Price Alert API",
        "endpoints": {
            "price_alert": "/price-alert?coin=bitcoin&target_price=1000000",
            "health": "/health"
        },
        "supported_coins": ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"]
    }

@app.get("/price-alert")
async def price_alert(coin: str = Query(...), target_price: float = Query(...)):
    """Check if a cryptocurrency has reached the target price"""
    result = await check_price_alert(coin, target_price)
    return result

