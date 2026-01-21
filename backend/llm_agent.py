def explain(metrics: dict):
    return (
        f"Based on historical data, the company {metrics['symbol']} "
        f"has a total return of {metrics['total_return']}, "
        f"with volatility {metrics['volatility']}. "
        f"Therefore, the decision is {metrics['decision']}."
    )
