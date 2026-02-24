def explain(metrics: dict):
    """
    Generates a professional financial summary based on calculated metrics.
    """
    symbol = metrics['symbol']
    total_ret = metrics['total_return'] * 100  # Convert to percentage
    vol = metrics['volatility']
    decision = metrics['decision']

    # Custom insights based on the decision
    if decision == "INVEST":
        insight = (f"{symbol} demonstrates exceptional growth potential with a "
                   f"robust {total_ret:.2f}% return. The risk-to-reward ratio is "
                   "highly favorable for long-term positions.")
    elif decision == "HOLD":
        insight = (f"{symbol} shows stable performance. While the {total_ret:.2f}% "
                   "return is positive, market fluctuations suggest a cautious "
                   "approach before increasing exposure.")
    else:
        insight = (f"The data for {symbol} indicates significant underperformance or "
                   f"high risk. With a return profile of {total_ret:.2f}%, current "
                   "signals suggest capital preservation over entry.")

    return (
        f"**Executive Summary for {symbol}:** {insight} "
        f"Technical analysis confirms a volatility index of {vol:.4f}. "
        f"Final Recommendation: **{decision}**."
    )