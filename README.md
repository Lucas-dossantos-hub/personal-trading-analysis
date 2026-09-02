# Personal Trading Analysis - Fama-French Factor Decomposition

## Overview
This project analyzes my personal trading performance using the Fama-French 3-Factor model to decompose returns into:
-Market exposure (Beta) - Exposure to broad market movements
-Size effect (SMB) - Exposure to small-cap vs large-cap stocks
-Value effect (HML) - Exposure to value vs growth stocks
-Alpha - Return not explained by the factors included in the model

---

## 🎯 Key Results

### GOOG Trade: +47.20% Return (June 4 - Sept 15, 2025)
- **Alpha: 23.80%** - Return not explained by the model
- **Market exposure: 11.11%** 
- **SMB/HML contribution: -1.65%**
- **Market performance during period: 9.09%**
- **Outperformance vs market: +38.11 percentage points**
- **R²: 0.2186** (21.86% of variance explained by factors)

**Interpretation:** The trade significantly outperformed the market over the holding period. The Fama-French model attributes a substantial part of the return to the intercept (alpha), while the relatively low R² indicates that the three factors explain only a limited share of the daily return variation.

---

### AAPL Trade: +27.67% Return (June 4, 2025 - April 13, 2026)
- **Alpha: 8.39%** - Return not explained by the model
- **Market exposure: 12.06%**
- **HML (Value) contribution: 4.28%**
- **SMB contribution: -1.10%**
- **Market performance during period: 11.48%**
- **Outperformance vs market: +16.19 percentage points**
- **R²: 0.2742** (27.42% of variance explained by factors)

**Interpretation:** The return was driven by a combination of market exposure, positive HML contribution and alpha. The positive HML contribution indicates that the portfolio's return benefited from exposure to the value factor during the holding period.
---

## 📊 Methodology

### Data Sources
- **Stock prices:** yfinance (Yahoo Finance)
- **Fama-French factors:** Kenneth French Data Library (daily factors)
- **Period:** Custom date ranges for each trade

### Analysis Steps
1. **Download** historical stock prices for entry/exit dates
2. **Calculate** daily returns using price changes
3. **Merge** stock returns with Fama-French factor data
4. **Fit** linear regression: `Excess Stock Return = Alpha + Beta_Market × Mkt-RF + Beta_SMB × SMB + Beta_HML × HML`
5. **Extract** alpha (intercept), betas (coefficients), R² (fit quality)
6. **Visualize** factor contributions and cumulative performance

### Key Metrics
- **Alpha:** Intercept of the regression, representing the average excess return not explained by the model factors
- **Beta:** Sensitivity of the stock's excess return to each factor
- **R²:** % of variance explained by the model
- **RMSE/MAE:** Model prediction error (lower is better)

---

## 📈 Visualizations

### Factor Attribution Charts
Bar charts showing how much each factor contributed to total returns:
- **Market Beta contribution**
- **SMB (Size) contribution**
- **HML (Value) contribution**
- **Alpha contribution** - Return attributed to the regression intercept

### Cumulative Returns Comparison
Line charts showing my returns vs individual Fama-French factors over time:
- Shows when I outperformed
- Shows factor performance during my holding period
- Shows the difference between total stock performance and factor-driven performance.
---

## 🛠️ How to Run

### Requirements
```bash
pip install pandas numpy scikit-learn yfinance plotly
```

### Run the Analysis
```bash
python code/trading_analysis_GOOG_AAPL.py
```

The script will:
1. Load Fama-French factors from CSV
2. Download stock price data
3. Calculate returns and fit regression model
4. Print detailed metrics
5. Display interactive Plotly charts

### Input Your Own Trades
Edit the `trades` dictionary in the script:
```python
trades = {
    "TICKER": {
        "entry_date": "YYYY-MM-DD",
        "entry_price": PRICE,
        "exit_date": "YYYY-MM-DD",
        "exit_price": PRICE,
        "return": CALCULATED_RETURN
    }
}
```

---

## 💡 Key Takeaways

- **Returns can have different sources:** The GOOG and AAPL trades show different combinations of market, SMB, HML and alpha contributions.
- **Factor exposure matters:** Comparing raw returns with factor-adjusted performance provides a more complete view of performance.
- **Model fit matters:** The relatively low R² values indicate that the three-factor model explains only part of the daily return variation.
- **Quantitative analysis provides context:** Regression-based attribution helps distinguish systematic factor exposure from returns not explained by the model.

---

## 📂 Project Contents

| File | Purpose |
|------|---------|
| `trading_analysis_GOOG_AAPL.py` | Main analysis of personal trades |
| `trading_analysis_NVDA.py` | Additional NVDA analysis / example |
| `results/` | Detailed regression metrics and outputs |
| `charts/` | Factor attribution and cumulative return charts |

---

## 🎓 Learning Resources

- **Kenneth French Data Library:** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- Fama-French (1993), *Common Risk Factors in the Returns on Stocks and Bonds*

---

## 📝 Conclusion

This project explores how Fama-French factor decomposition can be used to better understand individual trading performance.

By combining market data, factor data and regression analysis, the framework separates systematic factor exposure from returns not explained by the model.

The project also provided a practical application of Python to financial markets, covering data collection, statistical modelling and visualization.


---

## 📧 Contact

**Linkedin:** https://www.linkedin.com/in/lucas-dos-santos-620668329/

---

**Built with:** Python, Pandas, NumPy, Scikit-learn, yfinance, Plotly
