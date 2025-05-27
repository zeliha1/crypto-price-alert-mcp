async def check_price_alert(coin: str, target_price: float) -> dict:
    mock_prices = {
        "bitcoin": 3400000.0,
        "ethereum": 136000.0,
        "cardano": 34.0,
        "solana": 6800.0,
        "dogecoin": 1.36
    }

    coin_lower = coin.lower()

    if coin_lower not in mock_prices:
        return {"error": f"Coin '{coin}' bulunamadı"}

    current_price = mock_prices[coin_lower]
    reached = current_price >= target_price

    return {
        "coin": coin.upper(),
        "current_price": current_price,
        "target_price": target_price,
        "reached": reached
    }

