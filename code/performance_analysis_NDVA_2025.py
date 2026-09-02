#Load Fama-French factors from CSV
import pandas as pd

import pandas as pd

def load_fama_french(csv_path: str):
    df = pd.read_csv(csv_path, skiprows=4)

    # Rename first column to Date
    df = df.rename(columns={df.columns[0]: "Date"})

    # Convert Date
    df["Date"] = pd.to_datetime(
        df["Date"].astype(str),
        format="%Y%m%d")

    return df
    
csv_path = r"C:\Users\lucas\Documents\fama-french-backtest\data\raw\F-F_Research_Data_Factors_daily.csv"

df= load_fama_french(csv_path)

#Download stock price data using yfinance
#Calculate daily returns
import yfinance as yf

def load_stock_data(ticker :str, start :str, end :str):
    df = yf.download(ticker, start=start, end=end, progress =False)

    #Remove "NVDA" row
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    #Calcul return column
    df["Return"] = df["Close"].pct_change()
    return df
    
df_data = load_stock_data("NVDA", "2025-01-01", "2026-01-01")

print(df_data.describe())
#Merge/align the data by date
df = df.set_index("Date")
df_data.index = pd.to_datetime(df_data.index)

df_merged = df_data.join(df, how="inner")


#Create factor matrix X (Market, SMB, HML)
import numpy as np
#Delete empty rows
df_merged = df_merged.dropna()

df_merged[["Mkt-RF", "SMB", "HML", "RF"]] /= 100

X= df_merged[["Mkt-RF", "SMB", "HML"]].values

#Create excess return vector y (stock returns)
y = (df_merged["Return"] - df_merged["RF"]).values


print(df_merged[["Return", "Mkt-RF", "SMB", "HML", "RF"]].head())

#Verify data shapes match
if X.shape[0] == y.shape[0] :
    print("Shapes match!")
else : print(" Shapes Unmatch ;/")

#Fit LinearRegression model
from sklearn.linear_model import LinearRegression
model =LinearRegression()
model.fit(X, y)

#Extract: alpha, betas, r_squared
print("=" *100)
print(f"Daily Alpha: {model.intercept_*100:.4f}%")
print(f"Market Beta: {model.coef_[0]:.6f}")
print(f"SMB Beta: {model.coef_[1]:.6f}")
print(f"HML Beta: {model.coef_[2]:.6f}")

#Make predictions
new_market= 0.015
new_smb= 0.002
new_hml = -0.002
new_X = np.array([[new_market, new_smb, new_hml]])
predicted_excess_return= model.predict(new_X)[0]

predicted_return = predicted_excess_return + df_merged["RF"].mean()
print("="*100)
print(f"Predicted stock return : {predicted_return*100:.4f}%")

#Calculate residuals
predicted = model.predict(X)
residuals = df_merged["Return"] - predicted
print("="*100)
print(f"Mean residual: {residuals.mean()*100:.6f}%")
print(f"Residual std: {residuals.std()*100:.6f}%")

#Calculate R², MSE, RMSE, MAE
from sklearn.metrics import mean_squared_error, mean_absolute_error
r_squared = model.score(X,y)
mse = mean_squared_error(y, predicted)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y, predicted)

print("="*100)
print(f"R-Squared : {r_squared :.4f}")
print(f"MSE: {mse:.8f}")
print(f"RMSE: {rmse *100:.6f}%")
print(f"MAE: {mae *100:.6f}%")

#Check correlation matrix
print("="*100)
print("Correlation Matrix")
print(df_merged[["Return", "Mkt-RF", "SMB", "HML"]].corr())

#Chart 1: Stock price over time..............................................................................................
import plotly.graph_objects as go

fig = go.Figure(data = go.Scatter(
        x=df_data.index,
        y=df_data["Close"],
        mode="lines",
        name="NVDA",
        line = dict(color = 'blue', width = 2
    )))

fig.update_layout (
    title = "Stock price over time",
    xaxis_title = "Date",
    yaxis_title = "Price ($)" )

fig.show()

#Chart 2: Actual vs Predicted returns........................................................................................
fig = go.Figure()

fig.add_trace(go.Scatter(
        x=df_merged.index,
        y=y*100,
        mode="lines",
        name="Actual Return",
        line = dict(color="Green", width = 2)
    ))

fig.add_trace(go.Scatter(
        x=df_merged.index,
        y=predicted*100,
        mode="lines",
        name="Predicted Return",
        line = dict(color="Red", width = 2)
    ))

fig.update_layout(
    title="NVDA Actual vs Predicted Returns",
    xaxis_title="Date",
    yaxis_title="Excess Return (%)",
    template="plotly_white"
)

fig.show()
#Chart 3: Residuals distribution...............................................................................................
fig = go.Figure(go.Histogram(
        x=residuals*100,
        nbinsx=100,
        name="Residuals"
    ))

fig.update_layout(
    title="Distribution of NVDA Model Residuals",
    xaxis_title="Residual (%)",
    yaxis_title="Frequency",
    template="plotly_white"
)

fig.show()

#hart 4: Factor contributions..................................................................................................
# Calculate factor contributions
market_contribution = model.coef_[0] * df_merged["Mkt-RF"]
smb_contribution = model.coef_[1] * df_merged["SMB"]
hml_contribution = model.coef_[2] * df_merged["HML"]

# Average contribution over the sample
avg_contributions = [
    market_contribution.mean(),
    smb_contribution.mean(),
    hml_contribution.mean()
]

fig = go.Figure(go.Bar(
        x=["Market", "SMB", "HML"],
        y=[x * 100 for x in avg_contributions],
        name="Average Contribution"
    ))

fig.update_layout(
    title="Average Fama-French Factor Contributions to NVDA Returns",
    xaxis_title="Factor",
    yaxis_title="Average Contribution (%)",
    template="plotly_white"
)

fig.show()
