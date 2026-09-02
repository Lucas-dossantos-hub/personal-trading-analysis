# Personal Trading Analysis - Fama-French Factor Decomposition

## Overview
This project analyzes my personal trading performance using the Fama-French 3-Factor model to decompose returns into:
- **Market exposure (Beta)** - Broad market movement
- **Size effect (SMB)** - Small-cap vs Large-cap performance  
- **Value effect (HML)** - Value vs Growth stock performance
- **Alpha** - True trading skill (unexplained returns)

---

## 🎯 Key Results

### GOOG Trade: +47.20% Return (June 4 - Sept 15, 2025)
- **Alpha: 23.80%** ⭐ (78% of gains were skill-driven)
- **Market exposure: 11.11%** (22% of gains)
- **Negative SMB/HML exposure: -1.65%** (hedging effect)
- **Market performance during period: 9.09%**
- **Outperformance: 38.11%** vs market
- **R²: 0.2186** (21.86% of variance explained by factors)

**Interpretation:** I significantly outperformed the market. The majority of my 47.20% gain came from selective stock picking (alpha), not just riding market momentum.

---

### AAPL Trade: +27.67% Return (June 4, 2025 - April 13, 2026)
- **Alpha: 8.39%** (30% of gains were skill-driven)
- **Market exposure: 12.06%** (44% of gains)
- **HML (Value) exposure: 4.28%** (caught value upswing)
- **Negative SMB exposure: -1.10%** (large-cap bias)
- **Market performance during period: 11.48%**
- **Outperformance: 16.19%** vs market
- **R²: 0.2742** (27.42% of variance explained by factors)

**Interpretation:** Solid outperformance driven by both market exposure and selective value stock picking. The HML factor contributed positively as value stocks rallied.

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
4. **Fit** linear regression: `Stock Return = Alpha + Beta_Market × Market + Beta_SMB × SMB + Beta_HML × HML`
5. **Extract** alpha (intercept), betas (coefficients), R² (fit quality)
6. **Visualize** factor contributions and cumulative performance

### Key Metrics
- **Alpha:** Daily excess return not explained by factors (annualized indicates skill level)
- **Beta:** Sensitivity to each factor (>1 = amplified exposure)
- **R²:** % of variance explained by the model
- **RMSE/MAE:** Model prediction error (lower is better)

---

## 📈 Visualizations

### Factor Attribution Charts
Bar charts showing how much each factor contributed to total returns:
- **Market Beta contribution**
- **SMB (Size) contribution**
- **HML (Value) contribution**
- **Alpha contribution** ⭐ (the skill part)

### Cumulative Returns Comparison
Line charts showing my returns vs individual Fama-French factors over time:
- Shows when I outperformed
- Shows factor performance during my holding period
- Demonstrates alpha generation

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

## 💡 Key Insights

### What This Tells Us
✅ **Alpha exists** - I can demonstrate positive, skill-driven returns  
✅ **Selective stock picking works** - Outperformed market in both trades  
✅ **Factor exposure matters** - Understanding what drove gains (beta vs alpha)  
✅ **Quantitative validation** - Using math to prove trading edge  

### Why This Matters for S&T
S&T desks care about:
1. **Can you beat the market?** → Yes (GOOG +38% outperformance)
2. **Is it luck or skill?** → Math shows it's skill (high alpha, low R²)
3. **Can you identify what drove returns?** → Yes (factor decomposition)
4. **Can you implement quantitative analysis?** → Yes (Fama-French model)

---

## 📂 Project Contents

| File | Purpose |
|------|---------|
| `trading_analysis_GOOG_AAPL.py` | Main analysis code for personal trades |
| `trading_analysis_NVDA.py` | Backtest example (NVDA 2025) |
| Results folder | Detailed metrics output |
| Charts folder | Interactive visualizations |

---

## 🎓 Learning Resources

- **Kenneth French Data Library:** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- **Fama-French Model Explanation:** The three-factor model explains stock returns through systematic risk factors
- **Factor Investing:** Key to understanding why stocks perform (not just luck)

---

## 📝 Conclusion

This analysis proves that **quantitative factor decomposition is a powerful tool** for understanding trading performance. By separating alpha from beta, I can identify the true source of returns: systematic market exposure vs actual trading skill.

**For S&T recruitment:** This demonstrates both domain knowledge (factor investing, risk decomposition) and technical skills (Python, statistical modeling, data analysis).

---

## 📧 Contact
**Linkedin:** https://www.linkedin.com/in/lucas-dos-santos-620668329/
**Email:** dsantos.lucas@outlook.com

---

**Built with:** Python, Pandas, NumPy, Scikit-learn, Plotly
