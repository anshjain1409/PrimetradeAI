## 📌 Methodology

The analysis integrates **Bitcoin market sentiment (Fear vs. Greed)** with **historical trader-level data from Hyperliquid** to understand how sentiment impacts trading behavior and performance.

Data preprocessing involved integrity checks, timestamp alignment, and normalization of profitability using **PnL per dollar traded** to enable fair comparisons across traders with different capital sizes. To reduce distortion from extreme trades, **median-based metrics** were preferred over simple averages.

Traders were behaviorally segmented using **K-Means clustering**, identifying distinct trading archetypes based on trade frequency, position size, leverage, and risk-adjusted returns. Statistical validation was conducted using **non-parametric Mann–Whitney U tests** to confirm whether differences between Fear and Greed regimes were statistically significant.

Finally, a **Random Forest classifier** was trained to identify the most influential predictors of short-term profitability, enabling data-driven strategy formulation beyond descriptive analysis.

---

## 📊 Key Insights

* **Fear-driven overtrading**: Trade volume and frequency increase sharply during Fear regimes, while average profitability per trade declines, indicating panic-driven decision-making.
* **Greed improves efficiency**: Win rates and trade consistency are statistically higher during Greed phases, supporting momentum-driven market behavior.
* **Trader archetypes matter**: Low-frequency, high-precision traders ("Snipers") consistently outperform high-frequency, high-variance traders ("Gamblers"), particularly during volatile market conditions.
* **Momentum beats sentiment**: Recent trader performance (rolling win rate) is a stronger predictor of future profitability than market sentiment alone.

---

## 💡 Strategy Recommendations

1. **Anti-Fear Risk Control**

   * During Extreme Fear periods (Sentiment Index < 25), reduce leverage or temporarily halt trading activity.
   * This regime exhibits the highest downside volatility and weakest risk-adjusted returns across trader segments.

2. **Performance-Based Capital Allocation**

   * Allocate additional capital to traders with a **3-day rolling win rate above 60%**.
   * Short-term performance momentum emerged as the strongest alpha signal, outperforming sentiment-based indicators.

3. **Archetype-Aware Strategy Design**

   * Favor low-frequency, high-conviction trading styles during periods of high volatility.
   * Discourage excessive trade frequency during emotionally driven market phases to preserve capital and reduce drawdowns.
