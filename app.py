import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Crypto Trader Quant Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("Crypto Trader Performance vs. Market Sentiment")
st.markdown("### Interactive Quant Analysis Dashboard")

# --- 1. Data Loading ---
@st.cache_data
def load_data():
    try:
        # Load processed data
        df = pd.read_csv('dashboard_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.warning("⚠️ 'dashboard_data.csv' not found. Using Dummy Data for Demo.")
        # Generate Dummy Data
        dates = pd.date_range(start="2024-01-01", periods=100)
        data = {
            'date': dates,
            'daily_pnl': np.random.normal(100, 500, 100),
            'win_rate': np.random.uniform(0.3, 0.6, 100),
            'trade_count': np.random.randint(10, 100, 100),
            'sentiment_value': np.random.randint(10, 90, 100),
            'sentiment_category': np.random.choice(['Fear', 'Greed'], 100),
            'archetype': np.random.choice(['The Snipers', 'The Gamblers', 'The Whales'], 100)
        }
        return pd.DataFrame(data)

df = load_data()

# --- 2. Sidebar Filters ---
st.sidebar.header("🔍 Filters")

# Date Filter
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Categorical Filters
selected_clusters = st.sidebar.multiselect(
    "Select Trader Segments",
    options=df['archetype'].unique(),
    default=df['archetype'].unique()
)

selected_sentiments = st.sidebar.multiselect(
    "Select Market Sentiments",
    options=df['sentiment_category'].unique(),
    default=df['sentiment_category'].unique()
)

# Apply Filters
mask = (
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['archetype'].isin(selected_clusters)) &
    (df['sentiment_category'].isin(selected_sentiments))
)
filtered_df = df[mask]

st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df)}** records")

# --- 3. Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Market Overview", "🧠 Strategy Analysis", "🚀 Simulator"])

with tab1:
    st.subheader("Market Overview (The 'Big Picture')")
    
    # KPI Row
    col1, col2, col3 = st.columns(3)
    total_pnl = filtered_df['daily_pnl'].sum()
    avg_win_rate = filtered_df['win_rate'].mean()
    total_trades = filtered_df['trade_count'].sum()
    
    col1.metric("Total PnL", f"${total_pnl:,.0f}")
    col2.metric("Avg Win Rate", f"{avg_win_rate:.1%}")
    col3.metric("Total Trades Executed", f"{total_trades:,.0f}")
    
    st.markdown("---")
    
    # Dual Axis Chart
    st.markdown("#### volume vs. Sentiment Correlation")
    
    # Aggregating by date for the chart
    daily_agg = filtered_df.groupby('date').agg({
        'trade_count': 'sum',
        'sentiment_value': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    # Bar Chart (Volume)
    fig.add_trace(go.Bar(
        x=daily_agg['date'],
        y=daily_agg['trade_count'],
        name='Trade Volume',
        marker_color='lightblue',
        opacity=0.6
    ))
    
    # Line Chart (Sentiment)
    fig.add_trace(go.Scatter(
        x=daily_agg['date'],
        y=daily_agg['sentiment_value'],
        name='Sentiment Index',
        yaxis='y2',
        line=dict(color='orange', width=2)
    ))
    
    # Layout with Reference Bands
    fig.update_layout(
        title="Daily Volume vs Market Sentiment",
        yaxis=dict(title="Trade Volume"),
        yaxis2=dict(title="Sentiment Index", overlaying='y', side='right', range=[0, 100]),
        legend=dict(x=0.01, y=0.99),
        shapes=[
            # Fear Zone
            dict(type="rect", xref="paper", yref="y2", x0=0, x1=1, y0=0, y1=25, 
                 fillcolor="red", opacity=0.1, layer="below", line_width=0),
            # Greed Zone
            dict(type="rect", xref="paper", yref="y2", x0=0, x1=1, y0=75, y1=100, 
                 fillcolor="green", opacity=0.1, layer="below", line_width=0)
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Strategy Alpha Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Hypothesis H2: Win Rate vs Fear/Greed")
        fig_box = px.box(
            filtered_df, 
            x="sentiment_category", 
            y="win_rate", 
            color="sentiment_category",
            points="outliers",
            title="Win Rate Distribution by Sentiment"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.info("💡 **Insight**: Notice the median Win Rate is typically higher in Greed regimes, confirming momentum efficiency.")

    with col2:
        st.markdown("#### PnL Distribution (Risk Profile)")
        # Trimming extreme outliers for better visualization
        pnl_trim = filtered_df[filtered_df['daily_pnl'].between(-1000, 1000)]
        fig_hist = px.histogram(
            pnl_trim, 
            x="daily_pnl", 
            color="sentiment_category", 
            nbins=50, 
            marginal="box",
            title="Daily PnL Distribution (Trimmed ±$1000)"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.info("💡 **Insight**: Fear regimes often show 'fatter tails' on the left (losses), indicating higher blowout risk.")

with tab3:
    st.subheader("🚀 Interactive Strategy Simulator")
    st.markdown("Test the impact of our proposed **'Anti-Fear Strategy'** (Not trading when Sentiment < 25).")
    
    col1, col2, col3 = st.columns([1,1,2])
    
    start_cap = col1.number_input("Starting Capital ($)", value=10000, step=1000)
    strategy = col2.selectbox("Select Strategy", ["Buy & Hold (Benchmark)", "Anti-Fear Strategy (Smart Beta)"])
    
    # Simulator Logic
    sim_df = df.sort_values('date').copy()
    
    if strategy == "Anti-Fear Strategy":
        # Filter out trades on Days where Sentiment < 25
        sim_df = sim_df[sim_df['sentiment_value'] >= 25]
    
    # Calculate Equity Curve (Simple sum of PnL)
    sim_df['cumulative_pnl'] = sim_df['daily_pnl'].cumsum()
    sim_df['equity'] = start_cap + sim_df['cumulative_pnl']
    
    final_equity = sim_df['equity'].iloc[-1] if not sim_df.empty else start_cap
    roi = ((final_equity - start_cap) / start_cap) * 100
    
    # Display Result
    col3.metric("Final Equity", f"${final_equity:,.2f}", f"{roi:.1f}% ROI")
    
    st.line_chart(sim_df.set_index('date')['equity'])
    
    if strategy == "Anti-Fear Strategy":
        st.success(f"By filtering out Extreme Fear days, this strategy avoided **{len(df) - len(sim_df)}** high-risk trading days.")

st.markdown("---")
st.caption("Built for Crypto Hedge Fund • Powered by Streamlit & Plotly")
