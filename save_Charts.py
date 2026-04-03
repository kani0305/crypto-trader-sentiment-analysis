import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("merged_data.csv")
df['date'] = pd.to_datetime(df['date'])
df['profit'] = df['closed_pnl'] > 0

if not os.path.exists("charts"):
    os.makedirs("charts")

# Avg PnL
plt.figure()
df.groupby('classification')['closed_pnl'].mean().plot(kind='bar')
plt.title("Average PnL by Sentiment")
plt.savefig("charts/avg_pnl.png")
plt.close()

# Profit Rate
plt.figure()
df.groupby('classification')['profit'].mean().plot(kind='bar')
plt.title("Profit Rate")
plt.savefig("charts/profit_rate.png")
plt.close()

# Trade Count
plt.figure()
df['classification'].value_counts().plot(kind='bar')
plt.title("Trade Count")
plt.savefig("charts/trade_count.png")
plt.close()

# Boxplot
plt.figure()
sns.boxplot(x='classification', y='closed_pnl', data=df)
plt.title("PnL Distribution")
plt.savefig("charts/pnl_distribution.png")
plt.close()

# Time Trend
plt.figure()
df.groupby('date').size().plot()
plt.title("Trading Activity Over Time")
plt.savefig("charts/time_trend.png")
plt.close()

# Top Coins
plt.figure()
df.groupby('coin')['closed_pnl'].mean().sort_values(ascending=False).head(10).plot(kind='bar')
plt.title("Top Coins by Profit")
plt.savefig("charts/top_coins.png")
plt.close()

print("✅ Charts saved!")