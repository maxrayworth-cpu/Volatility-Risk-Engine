import pandas as pd
import numpy as np
from pricing import cleaned_pricing
from visualisation import render_3d_surface
from visualisation import volatility_smile



def main():
    print("--- Starting Volatility Surface Pipeline ---")
    print("Fetching data and calculating implied volatilities")
    clean_df, spot = cleaned_pricing()

    print(f"--- Successfully processed {len(clean_df)} option contracts")

# Add this line right after clean_df is created in main.py:
    print("\n--- TABLE 1 DATA ---\n", clean_df.groupby('expiration')['strike'].count().head(5))

    print("--- Generating 3D Volatility Surface")
    fig, grid_k, grid_t, grid_iv = render_3d_surface(
        clean_df, spot_price=spot
    )

    print("--- Generating 2D Volatility Smile")
    volatility_smile(
        grid_k=grid_k,
        grid_t=grid_t,
        grid_iv=grid_iv,
        target_t=0.5,
        spot_price=spot,  # Notice we pass 'spot' here instead of 'spot_price'
    )

    fig.show()


if __name__ == "__main__":
    main()





