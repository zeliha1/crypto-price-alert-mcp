# Mock veri ile test (API sorunları nedeniyle)
async def check_price_alert(coin: str, target_price: float) -> dict:
    # Mock kripto fiyatları (TRY cinsinden)
    mock_prices = {
        "bitcoin": 3400000.0,  # ~100k USD * 34
        "ethereum": 136000.0,  # ~4k USD * 34
        "cardano": 34.0,       # ~1 USD * 34
        "solana": 6800.0,      # ~200 USD * 34
        "dogecoin": 1.36       # ~0.04 USD * 34
    }

    coin_lower = coin.lower()

    if coin_lower not in mock_prices:
        return {"error": f"Coin '{coin}' bulunamadı. Desteklenen coinler: {', '.join(mock_prices.keys())}"}

    current_price = mock_prices[coin_lower]
    reached = current_price >= target_price

    return {
        "coin": coin.upper(),
        "current_price_try": current_price,
        "target_price": target_price,
        "reached": reached,
        "status": "Hedef fiyata ulaştı!" if reached else "Hedef fiyata henüz ulaşmadı",
        "note": "Bu demo verilerdir. Gerçek API entegrasyonu için SSL sertifika sorunu çözülmelidir."
    }

