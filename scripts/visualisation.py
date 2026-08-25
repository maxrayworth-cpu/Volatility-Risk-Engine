import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

def volatility_smile(
    grid_k, grid_t, grid_iv, target_t=0.50, spot_price=None
):
    t_axis = grid_t[:, 0]  
    t_idx = np.argmin(np.abs(t_axis - target_t))
    actual_t = t_axis[t_idx]

    strikes = grid_k[t_idx, :]
    iv_slice = grid_iv[t_idx, :]

    plt.figure(figsize=(10,8))
    plt.plot(
        strikes,
        iv_slice,
        label=f"T = {actual_t:.2f} yrs",
        color="#1f77b4",
        linewidth=2.5,
    )

    if spot_price is not None:
        plt.axvline(
            x=spot_price,
            color="red",
            linestyle="--",
            alpha=0.7,
            label=f"Spot Price (${spot_price:.2f})",
        )

    plt.title(
        f"Implied Volatility Smile at T ≈ {actual_t:.2f} Years",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Strike Price ($)", fontsize=12)
    plt.ylabel("Implied Volatility (σ)", fontsize=12)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()


def render_3d_surface(plot_df, spot_price=None):     

    
    x_line = np.linspace(plot_df['strike'].min(), plot_df['strike'].max(),100)
    y_line = np.linspace(plot_df['timeToMaturity'].min(), plot_df['timeToMaturity'].max(),100)

    X, Y = np.meshgrid(x_line,y_line)

    Z = griddata(
        points=(plot_df['strike'], plot_df['timeToMaturity']),
        values=plot_df['impliedVolatility'],
        xi=(X, Y),
        method='linear'
    )

    Z_nearest = griddata(
        (plot_df["strike"], plot_df["timeToMaturity"]),
        plot_df["impliedVolatility"],
        (X, Y),
        method="nearest",
    )

    Z = np.where(np.isnan(Z), Z_nearest, Z)
    Z_smoothed = gaussian_filter(Z, sigma=1.25)

    surface = go.Surface(
        x=X, y=Y, z=Z_smoothed,
        colorscale = 'Viridis',
        colorbar=dict(title="Implied Volatility (σ)"),
        name="IV Surface",
    )

    fig = go.Figure(data=[surface])

    if spot_price is not None:
        min_time = plot_df["timeToMaturity"].min()
        z_min = Z_smoothed.min()
        z_max = Z_smoothed.max()

    fig.add_trace(
        go.Scatter3d(
            x=[spot_price, spot_price],
            y=[min_time, min_time],
            z=[z_min, z_max],
            mode="lines",
            line=dict(color="red", width=6),
            name=f"Spot Price (${spot_price:.2f})",
        )
    )

    fig.update_layout(
        title = 'SPY Implied Volatility Surface',
        autosize = False,
        width = 900,
        height = 700,
        scene=dict(
            xaxis=dict(title='Strike Price ($)'),
            yaxis=dict(title='Time to Maturity (yrs)'),
            zaxis=dict(title='Implied Volatility (σ)')
        )
    )
    
    
    return fig, X, Y, Z_smoothed


