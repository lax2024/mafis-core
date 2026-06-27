def generate_signal(rsi, macd, macd_signal, price, sma50, sma200):
    score = 0
    reasons = []

    if rsi < 30:
        score += 1
        reasons.append("RSI indicates oversold")
    elif rsi > 70:
        score -= 1
        reasons.append("RSI indicates overbought")

    if macd > macd_signal:
        score += 1
        reasons.append("MACD bullish crossover")
    else:
        score -= 1
        reasons.append("MACD bearish crossover")

    if price > sma50:
        score += 1
        reasons.append("Price above SMA50")

    if sma50 > sma200:
        score += 1
        reasons.append("Golden crossover")

    if score >= 3:
        return "BUY", 0.80, reasons
    elif score >= 1:
        return "HOLD", 0.60, reasons
    else:
        return "SELL", 0.70, reasons