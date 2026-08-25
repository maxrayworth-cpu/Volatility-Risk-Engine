import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from data_fetcher import fetch_options_data


def black_scholes_call(S, K, sigma, T, r=0.05):
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * (sigma**2)) * T) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    C = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return C


def iv_call(market_price, S, K, T, r=0.05):
    if market_price <= 0 or T <= 0:
        return np.nan

    def objective_function(sigma):
        return black_scholes_call(S, K, sigma, T, r) - market_price

    try:
        return brentq(objective_function, 0.0001, 5.0)
    except Exception:
        return np.nan


def cleaned_pricing():
    df, spot = fetch_options_data("SPY")
    
    df["impliedVolatility"] = df.apply(
        lambda row: iv_call(
            row["midPrice"], spot, row["strike"], row["timeToMaturity"], r=0.05
        ),
        axis=1,
    )

    clean_df = df.dropna(subset=["impliedVolatility"])

    clean_df = clean_df[
        (clean_df["impliedVolatility"] > 0.05) &
        (clean_df["impliedVolatility"] < 0.80) &
        (clean_df["strike"] >= 0.70 * spot) &
        (clean_df["strike"] <= 1.30 * spot) &
        (clean_df['timeToMaturity'] >= 0.05)
    ]

    return clean_df, spot


if __name__ == "__main__":
    clean_df, spot = cleaned_pricing()
    print(f"Calculated IVs for {len(clean_df)} valid options contracts")
    print(clean_df[["strike", "timeToMaturity", "midPrice", "impliedVolatility"]])

