import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import yfinance as yf
import plotly.graph_objects as go

#Load FF ==========================================================================================================================
def load_fama_french(csv_path: str):
    df = pd.read_csv(csv_path, skiprows=4)

    # Rename first column to Date
    df = df.rename(columns={df.columns[0]: "Date"})

    # Convert Date
    df["Date"] = pd.to_datetime(
        df["Date"].astype(str),
        format="%Y%m%d"
    )

    return df
    
csv_path = r"C:\Users\lucas\Documents\fama-french-backtest\data\raw\F-F_Research_Data_Factors_daily.csv"

df= load_fama_french(csv_path)
df = df.set_index("Date")



# MY TRADES DATAS ==================================================================================================================
trades = {
    "GOOG": {
        "entry_date": "2025-06-04",
        "entry_price": 167.42,
        "exit_date": "2025-09-15",
        "exit_price": 246.45,
        "return": 0.4720
    },
    "AAPL": {
        "entry_date": "2025-06-04",
        "entry_price": 202.89,
        "exit_date": "2026-04-13",
        "exit_price": 259.03,
        "return": 0.2767
    }
}

#FF Analysis ========================================================================================================================
for ticker, trade in trades.items():

    print(f"\nAnalyzing {ticker}...")

    # Download stock prices
    stock = yf.download(
        ticker,
        start=trade["entry_date"],
        end=trade["exit_date"],
        auto_adjust=True,
        progress=False
    )


    #Remove ticker level 
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)
        
    # Daily stock returns
    stock_returns = stock["Close"].squeeze().pct_change().dropna()
    stock_returns.name = "Return"

    # Select Fama-French data for the trade period
    ff = df.loc[
        trade["entry_date"]:trade["exit_date"]
    ].copy()

    ff[["Mkt-RF", "SMB", "HML", "RF"]] /= 100

    # Merge stock returns with Fama-French factors =====================================================================================
    data = pd.concat(
        [stock_returns, ff],
        axis=1,
        sort= False
    ).dropna()

    # Excess stock return
    data["Excess_Return"] = data["Return"] - data["RF"]

    #Regression
    X = data[["Mkt-RF", "SMB", "HML"]].values
    y = data["Excess_Return"].values

    model = LinearRegression()
    model.fit(X, y)

    # Predictions
    predicted = model.predict(X)

    # Residuals
    residuals = y - predicted

    # Metrics
    r_squared = model.score(X, y)
    mse = mean_squared_error(y, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, predicted)

    # Results
    print(f"Alpha: {model.intercept_:.6f}")
    print(f"Market Beta: {model.coef_[0]:.6f}")
    print(f"SMB Beta: {model.coef_[1]:.6f}")
    print(f"HML Beta: {model.coef_[2]:.6f}")
    print(f"R-Squared: {r_squared:.4f}")
    print(f"RMSE: {rmse * 100:.4f}%")
    print(f"MAE: {mae * 100:.4f}%")

    # Factor performance during trade
    market_return = (1 + data["Mkt-RF"]).prod() - 1
    smb_return = (1 + data["SMB"]).prod() - 1
    hml_return = (1 + data["HML"]).prod() - 1

    print("\nFactor Performance During Trade:")
    print(f"Market (Mkt-RF): {market_return * 100:.2f}%")
    print(f"SMB: {smb_return * 100:.2f}%")
    print(f"HML: {hml_return * 100:.2f}%")

     # Factor contributions
    market_contribution = model.coef_[0] * data["Mkt-RF"].sum()
    smb_contribution = model.coef_[1] * data["SMB"].sum()
    hml_contribution = model.coef_[2] * data["HML"].sum()
    alpha_contribution = model.intercept_ * len(data)

    print("\nFactor Contributions:")
    print(f"Market: {market_contribution * 100:.2f}%")
    print(f"SMB: {smb_contribution * 100:.2f}%")
    print(f"HML: {hml_contribution * 100:.2f}%")
    print(f"Alpha: {alpha_contribution * 100:.2f}%")

   # Bar Chart ==================================================================================
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Market", "SMB", "HML", "Alpha"],
            y=[
                market_contribution * 100,
                smb_contribution * 100,
                hml_contribution * 100,
                alpha_contribution * 100
            ]
        )
    )

    fig.update_layout(
        title=f"{ticker} - Fama-French Return Attribution",
        xaxis_title="Factor",
        yaxis_title="Contribution (%)",
        template="plotly_white"
    )

    fig.show()
    
    # Cumulative Returns Chart ====================================================================

    data["Trade_Cumulative"] = (1 + data["Return"]).cumprod() - 1
    data["Market_Cumulative"] = (1 + data["Mkt-RF"]).cumprod() - 1
    data["SMB_Cumulative"] = (1 + data["SMB"]).cumprod() - 1
    data["HML_Cumulative"] = (1 + data["HML"]).cumprod() - 1

    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Trade_Cumulative"] * 100,
        mode="lines",
        name=ticker
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Market_Cumulative"] * 100,
            mode="lines",
            name="Market"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMB_Cumulative"] * 100,
            mode="lines",
            name="SMB"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["HML_Cumulative"] * 100,
            mode="lines",
            name="HML"
        )
    )

    fig.update_layout(
        title=f"{ticker} - Cumulative Returns vs Fama-French Factors",
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        template="plotly_white"
    )

    fig.show()
