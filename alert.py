import httpx

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

async def check_price_alert(coin: str, target_price: float) -> dict:
    params = {
        "ids": coin.lower(),
        "vs_currencies": "try"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(COINGECKO_API, params=params)
        data = response.json()

    if coin.lower() not in data:
        return {"error": "Coin bulunamadı"}

    current_price = data[coin.lower()]["try"]
    reached = current_price >= target_price

    return {
        "coin": coin.upper(),
        "current_price": current_price,
        "target_price": target_price,
        "reached": reached
    }

