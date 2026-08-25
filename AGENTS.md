# Volatility Risk Engine – Agent Instructions

## Project Overview
This is a Python-based quantitative finance engine that prices options and analyzes volatility using the Black-Scholes model. It fetches real-time options data from Yahoo Finance and computes implied volatility.

**Tech Stack**: Python 3.x | NumPy, SciPy, Pandas | yfinance

## Architecture

### Core Components
- **`scripts/data_fetcher.py`**: Fetches options chains and spot prices from Yahoo Finance API. Returns clean DataFrame with strike, expiration, bid/ask, mid-price, and time-to-maturity.
- **`scripts/pricing.py`**: Contains Black-Scholes option pricing model and implied volatility calculation. Imports `data_fetcher` module.

### Data Pipeline
1. User specifies ticker symbol (e.g., "SPY", "AAPL")
2. `fetch_options_data()` retrieves live option chains
3. Data is cleaned (removes zero bids, low volume)
4. Pricing functions compute theoretical values and implied volatility

## Key Conventions

### Python Style
- Include docstrings for public functions with Returns section
- Use inline comments for complex financial calculations
- Test functions with `if __name__ == "__main__"` blocks (see `data_fetcher.py`)

### Financial Constants
- Risk-free rate `r = 0.05` (5%) is the default
- Time-to-maturity `T` is always in years (convert days by dividing by 365)
- Skip options expiring in ≤1 day to avoid numerical instability

### Data Handling
- Use `yfinance` for market data (no local databases)
- Store option chains as Pandas DataFrames
- Column names use camelCase (`timeToMaturity`, `midPrice`, `daysToExpiration`)
- Filter out noisy options: `bid > 0`, `ask > 0`, `volume > 5`

## Development Setup

### Environment
- Virtual environment in `.venv/` is pre-configured
- Python interpreter configured in `.vscode/settings.json`

### Dependencies
Currently imported in source:
- `yfinance` (market data)
- `pandas` (data frames)
- `numpy` (numerical operations)
- `scipy.stats` + `scipy.optimize` (distributions, optimization)

**TODO**: Create `requirements.txt` or `pyproject.toml` for reproducibility.

## Known Issues & Pitfalls

1. **Syntax Error in `pricing.py` (Line 5)**
   - `sigma` parameter has no default value: `def black_scholes_call(S, K, T, r = 0.05, sigma):`
   - Fix: Add default, e.g., `sigma=0.2`

2. **Incomplete Implementation**
   - `implied_volatility_call()` function is not finished (cuts off mid-implementation)
   - Uses `scipy.optimize.brentq` but import is unused

3. **Missing Documentation**
   - `docs/` folder is empty
   - No design docs, algorithm references, or test cases

4. **No Test Suite**
   - Manual testing only via `if __name__ == "__main__"` blocks
   - Consider adding unit tests for numerical stability

## Common Tasks

### Run Data Fetcher
```bash
cd /Users/maxrayworth/Desktop/Summer\ 2026\ Work/Volatility-Risk-Engine
python scripts/data_fetcher.py
```
Expected output: Prints current spot price, number of liquid calls, and sample data table.

### Debug Pricing Module
```bash
python scripts/pricing.py
```
Currently fails due to syntax error. Fix the default parameter first.

### Add a New Ticker
Edit the `if __name__ == "__main__"` block in `data_fetcher.py`, change `symbol = "SPY"` to your target.

## Recommended Next Steps for Agents

- **Fix syntax errors** in `pricing.py` before attempting to use pricing functions
- **Complete `implied_volatility_call()`** – implement the optimization loop
- **Create `requirements.txt`** to document dependencies and versions
- **Add unit tests** for Black-Scholes calculation against known benchmark values
- **Document financial assumptions** (e.g., European vs. American options, dividend handling)

## Quick Reference: Black-Scholes Model

The engine implements the standard European call option pricing formula:
- **d1** = (ln(S/K) + (r + σ²/2)·T) / (σ·√T)
- **d2** = d1 − σ·√T
- **C** = S·N(d1) − K·e^(−rT)·N(d2)

Where: S = spot price, K = strike, T = time to maturity (years), r = risk-free rate, σ = volatility, N = normal CDF.
