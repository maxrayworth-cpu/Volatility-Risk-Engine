import yfinance as yf # Connects to Yahoo Finance API
import pandas as pd # Library for data manipulation and analysis    
import numpy as np # Library for numerical operations
from datetime import datetime # Library for handling date arithmetic

def fetch_options_data(ticker_symbol): # Represents the asset of interest
    """
    Fetches call option chains and current spot price for a given ticker.
    Returns:
        df (pd.DataFrame): Processed option data containing Strike, Expiry, Days/Years to Expiry,
                           Bid, Ask, Mid Price, and Volume.
        spot_price (float): Current price of the underlying asset.
    """
    print(f"Fetching market data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    
    history = ticker.history(period="1d") # Pulls most recent 1-day trading history to extract current spot price
    if history.empty:
        raise ValueError(f"Could not fetch historical price data for {ticker_symbol}.") # Handles error if ticker returns no data
    spot_price = history['Close'].iloc[-1]
    
    # 2. Iterate through option exspirations
    expirations = ticker.options # Retrieves all available expiration dates 
    all_calls = []
    
    today = datetime.now()
    
    for exp in expirations:
        # Calculate time to maturity in years (T)
        exp_date = datetime.strptime(exp, "%Y-%m-%d") # Converts string dates into datetime objects
        days_to_exp = (exp_date - today).days # Calculates number of days until expiration
        
        # Skip options expiring today or in the past to avoid zero-division issues in pricing models
        if days_to_exp <= 1:
            continue # Avoids asymptotic results in pricing models
            
        T = days_to_exp / 365.0 # Calculates time in years to conform with Black-Scholes model
        
        chain = ticker.option_chain(exp) # Pull call options chain
        calls = chain.calls.copy() 
        
    # Adds metadata columns 
        calls['expiration'] = exp
        calls['daysToExpiration'] = days_to_exp
        calls['timeToMaturity'] = T 
        calls['midPrice'] = (calls['bid'] + calls['ask']) / 2.0 # Best way of estimating the option's fair price right now 
        
        all_calls.append(calls)
        
    
    master_df = pd.concat(all_calls, ignore_index=True) # Combines into one large dataframe
    
    # Remove options with zero bid/ask or low volume to remove noise
    clean_df = master_df[
        (master_df['bid'] > 0) & 
        (master_df['ask'] > 0) & 
        (master_df['volume'] > 5)
    ].copy()
    
    # Remove any unnecessary columns from the Yahoo Finance API
    final_cols = ['strike', 'expiration', 'daysToExpiration', 'timeToMaturity', 
                  'bid', 'ask', 'midPrice', 'lastPrice', 'volume', 'openInterest']
    
    return clean_df[final_cols], spot_price


# Quick execution block to test when running this file directly
if __name__ == "__main__":
    # Test with S&P 500 ETF (SPY) or Apple (AAPL)
    symbol = "SPY"
    df, spot = fetch_options_data(symbol)
    
    print(f"\nSuccessfully fetched data for {symbol}")
    print(f"Current Spot Price: ${spot:.2f}")
    print(f"Total Liquid Call Option Contracts Found: {len(df)}")
    print("\nFirst 10 rows of data:")
    pd.set_option('display.max_columns', None)
    print(df.head(10))
          
