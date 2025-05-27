from fastapi import FastAPI, Query
from alert import check_price_alert

app = FastAPI()

@app.get("/price-alert")
async def price_alert(coin: str = Query(...), target_price: float = Query(...)):
    result = await check_price_alert(coin, target_price)
    return result

