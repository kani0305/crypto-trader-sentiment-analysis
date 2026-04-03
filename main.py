# ==============================
# IMPORT
# ==============================
import pandas as pd

# ==============================
# LOAD DATA
# ==============================
trader_df = pd.read_csv("historical_data.csv")
sentiment_df = pd.read_csv("fear_greed_index.csv")

# ==============================
# CLEAN COLUMNS
# ==============================
trader_df.columns = trader_df.columns.str.strip().str.lower().str.replace(" ", "_")
sentiment_df.columns = sentiment_df.columns.str.strip().str.lower().str.replace(" ", "_")

# ==============================
# FIX DATES
# ==============================
trader_df['timestamp_ist'] = pd.to_datetime(trader_df['timestamp_ist'], dayfirst=True, errors='coerce')
trader_df['date'] = trader_df['timestamp_ist'].dt.date

sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

# Simplify sentiment
sentiment_df['classification'] = sentiment_df['classification'].replace({
    'Extreme Fear': 'Fear',
    'Extreme Greed': 'Greed'
})

# ==============================
# MERGE
# ==============================
merged_df = trader_df.merge(sentiment_df, on='date', how='left')

# ==============================
# SAVE
# ==============================
merged_df.to_csv("merged_data.csv", index=False)

print("✅ Data merged and saved!")