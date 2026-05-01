import pandas as pd
import matplotlib.pyplot as plt

# Load merged data
df = pd.read_csv("data/processed/merged_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Clean text
df["classification"] = df["classification"].astype(str).str.strip().str.lower()
df["side"] = df["side"].astype(str).str.strip().str.lower()

# Keep only rows with valid sentiment for sentiment charts
sentiment_df = df[df["classification"].isin([
    "extreme fear", "fear", "neutral", "greed", "extreme greed"
])].copy()

# Create output folder if needed
import os
os.makedirs("outputs/figures", exist_ok=True)

# 1) Average PnL by sentiment
sentiment_avg = sentiment_df.groupby("classification")["closed_pnl"].mean().reindex(
    ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
)
plt.figure(figsize=(10, 6))
sentiment_avg.plot(kind="bar")
plt.title("Average Closed PnL by Market Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Average Closed PnL")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/figures/avg_pnl_by_sentiment.png", dpi=300)
plt.close()

# 2) Win rate by sentiment
win_rate = sentiment_df.groupby("classification")["closed_pnl"].apply(lambda x: (x > 0).mean()).reindex(
    ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
)
plt.figure(figsize=(10, 6))
win_rate.plot(kind="bar")
plt.title("Win Rate by Market Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Win Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/figures/win_rate_by_sentiment.png", dpi=300)
plt.close()

# 3) Total PnL by sentiment
total_pnl = sentiment_df.groupby("classification")["closed_pnl"].sum().reindex(
    ["extreme fear", "fear", "neutral", "greed", "extreme greed"]
)
plt.figure(figsize=(10, 6))
total_pnl.plot(kind="bar")
plt.title("Total Closed PnL by Market Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Total Closed PnL")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/figures/total_pnl_by_sentiment.png", dpi=300)
plt.close()

# 4) Buy vs Sell average PnL by sentiment
pivot = sentiment_df.pivot_table(
    index="classification",
    columns="side",
    values="closed_pnl",
    aggfunc="mean"
).reindex(["extreme fear", "fear", "neutral", "greed", "extreme greed"])

plt.figure(figsize=(10, 6))
pivot.plot(kind="bar")
plt.title("Average Closed PnL by Sentiment and Side")
plt.xlabel("Sentiment")
plt.ylabel("Average Closed PnL")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/figures/avg_pnl_side_sentiment.png", dpi=300)
plt.close()

# 5) Top 10 accounts by total PnL
top_accounts = df.groupby("account")["closed_pnl"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_accounts.plot(kind="bar")
plt.title("Top 10 Accounts by Total Closed PnL")
plt.xlabel("Account")
plt.ylabel("Total Closed PnL")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("outputs/figures/top_10_accounts.png", dpi=300)
plt.close()

print("Visualizations created successfully.")