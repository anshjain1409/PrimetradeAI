# Crypto Trader Performance vs. Market Sentiment Analysis

## 🎯 Objective

This project analyzes how Bitcoin market sentiment (Fear vs. Greed) influences trader behavior and performance on Hyperliquid. By applying advanced quantitative methods, we uncover behavioral patterns to inform smarter, data-driven trading strategies.

## 📂 Project Structure

- `app.py`: **Streamlit Dashboard** visualizing the analysis.
- `dashboard_data.csv`: Processed data powering the dashboard.
- `notebooks/Trader_Performance_Analysis.ipynb`: **Core Analysis Notebook** containing rigorous Quant Analysis.
- `data/`: Contains raw datasets (`fear_greed_index.csv`, `historical_data.csv`).
- `requirements.txt`: Python dependencies.

## 🚀 How to Run

### 1. Run the Analysis Notebook

To regenerate the analysis and data:

```bash
jupyter notebook notebooks/Trader_Performance_Analysis.ipynb
```

### 2. Launch the Dashboard

To explore the interactive insights:

```bash
streamlit run app.py
```

---

## 🧠 Methodology

Our analysis goes beyond basic correlations by employing professional Data Science techniques:

1.  **Robust Data Engineering & Profiling**:
    - **Data Integrity Check**:
      - `historical_data.csv`: **211,224 rows**, **16 columns**, **0 missing values**.
      - `fear_greed_index.csv`: **2,644 rows**, **4 columns**, **0 missing values**.
    - **Normalization**: Calculated **PnL per Dollar Traded** (ROE Proxy) to normalize performance across different account sizes.
    - **Outlier Handling**: Used **Median Position Sizes** instead of averages to mitigate skew from outlier trades.

2.  **Advanced Segmentation (Clustering)**:
    - Applied **K-Means Clustering** to mathematically identify 3 distinct Trader Archetypes based on behavior:
      - **The Snipers**: High Win Rate, Low Frequency.
      - **The Gamblers**: High Frequency, High Variance.
      - **The Whales**: Large Position Sizes.

3.  **Statistical Rigor**:
    - Utilized **Mann-Whitney U Tests** to confirm that performance differences between "Fear" and "Greed" regimes are statistically significant (p-values < 0.05), moving beyond simple observations.

4.  **Predictive Modeling (Alpha)**:
    - Built a **Random Forest Classifier** to identify the top predictors of next-day profitability.

## 📊 Key Insights

- **Panic Volume**: Trade frequency spikes significantly during "Fear" periods, but per-trade profitability drops. This confirms "panic selling" behavior among retail traders.
- **Greed Efficiency**: Win rates are statistically higher (~42%) during "Greed" regimes, validating momentum strategies in euphoric markets.
- **Archetype Performance**: "The Snipers" consistently outperform "The Gamblers", particularly during high-volatility events, proving that patience yields higher Sharpe ratios.

## 💡 Strategy Recommendations

Based on our quantitative findings, we propose two actionable rules:

1.  **The "Anti-Fear" Circuit Breaker**:
    - **Rule**: When Sentiment Index < 25 (Extreme Fear), restrict trading leverage to 1x or halt completely.
    - **Data Backing**: Our analysis shows that negative PnL variance is highest in this regime for widespread trader segments.

2.  **Momentum Allocation ("Hot Hand")**:
    - **Rule**: Allocate more capital to traders whose 3-Day Rolling Win Rate > 60%.
    - **Data Backing**: Our Random Forest model identified **Recent Win Rate Momentum** as the #1 strongest predictor of future profitability, outperforming the Sentiment Index itself.

## Streamlit App Link : https://primetradeai-20261409.streamlit.app/
