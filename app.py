import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Intelligence", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("merged_data.csv")
    df['profit'] = df['closed_pnl'] > 0
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

st.title("🧠 Trader Behavior Intelligence Dashboard")

# ================= FILTERS =================
st.markdown("## 🔍 Filters")
col1, col2, col3 = st.columns(3)

with col1:
    sentiment = st.multiselect("Sentiment", sorted(df['classification'].dropna().unique()))

with col2:
    coin = st.multiselect("Coin", sorted(df['coin'].dropna().unique()))

with col3:
    date_range = st.date_input("Date Range", [df['date'].min(), df['date'].max()])

# Apply filters
filtered_df = df.copy()

if sentiment:
    filtered_df = filtered_df[filtered_df['classification'].isin(sentiment)]

if coin:
    filtered_df = filtered_df[filtered_df['coin'].isin(coin)]

filtered_df = filtered_df[
    (filtered_df['date'] >= pd.to_datetime(date_range[0])) &
    (filtered_df['date'] <= pd.to_datetime(date_range[1]))
]

st.markdown("---")

# ================= KPIs =================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg PnL", round(filtered_df['closed_pnl'].mean(), 2))
col2.metric("Profit Rate", round(filtered_df['profit'].mean(), 2))
col3.metric("Trades", len(filtered_df))
col4.metric("Avg Size", round(filtered_df['size_usd'].mean(), 2))

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs(["Performance", "Risk", "Behavior", "Insights"])

with tab1:
    st.bar_chart(filtered_df.groupby('classification')['closed_pnl'].mean())
    st.bar_chart(filtered_df.groupby('classification')['profit'].mean())

with tab2:
    fig, ax = plt.subplots()
    sns.boxplot(x='classification', y='closed_pnl', data=filtered_df, ax=ax)
    st.pyplot(fig)

with tab3:
    st.bar_chart(filtered_df['classification'].value_counts())

with tab4:
    st.line_chart(filtered_df.groupby('date').size())

    top_coins = filtered_df.groupby('coin')['closed_pnl'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(top_coins)

# Strategy
st.markdown("## Strategy Insight")

fear = filtered_df[filtered_df['classification'] == 'Fear']['closed_pnl'].mean()
greed = filtered_df[filtered_df['classification'] == 'Greed']['closed_pnl'].mean()

if fear > greed:
    st.success("Better in Fear → Contrarian Strategy")
else:
    st.warning("Better in Greed → Momentum Strategy")