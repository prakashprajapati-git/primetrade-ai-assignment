import pandas as pd
import numpy as np
import os

# Load merged data
df = pd.read_csv("data/processed/merged_data.csv")

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Ensure numeric columns are numeric
for col in ["closed_pnl", "size_usd", "execution_price", "sentiment_score", "fee"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean text columns
if "classification" in df.columns:
    df["classification"] = df["classification"].astype(str).str.strip().str.lower()

if "side" in df.columns:
    df["side"] = df["side"].astype(str).str.strip().str.lower()

# Keep only valid sentiment labels for sentiment-based analysis
valid_sentiments = [
    "extreme fear",
    "fear",
    "neutral",
    "greed",
    "extreme greed"
]
df_valid = df[df["classification"].isin(valid_sentiments)].copy()

# Create output folders if missing
os.makedirs("outputs/tables", exist_ok=True)

# -------------------------------
# OVERALL SUMMARY
# -------------------------------
overall_summary = pd.DataFrame({
    "metric": [
        "total_trades",
        "unique_accounts",
        "total_closed_pnl",
        "avg_closed_pnl_per_trade",
        "median_closed_pnl_per_trade",
        "win_rate"
    ],
    "value": [
        len(df),
        df["account"].nunique() if "account" in df.columns else np.nan,
        df["closed_pnl"].sum(),
        df["closed_pnl"].mean(),
        df["closed_pnl"].median(),
        (df["closed_pnl"] > 0).mean()
    ]
})

# -------------------------------
# SENTIMENT-WISE PERFORMANCE
# -------------------------------
sentiment_perf = (
    df_valid.groupby("classification")
    .agg(
        trades=("closed_pnl", "size"),
        total_pnl=("closed_pnl", "sum"),
        avg_pnl=("closed_pnl", "mean"),
        median_pnl=("closed_pnl", "median"),
        win_rate=("closed_pnl", lambda x: (x > 0).mean()),
        avg_size_usd=("size_usd", "mean")
    )
    .reset_index()
    .sort_values("total_pnl", ascending=False)
)

# -------------------------------
# SENTIMENT SCORE PERFORMANCE
# -------------------------------
score_perf = (
    df_valid.groupby("sentiment_score")
    .agg(
        trades=("closed_pnl", "size"),
        total_pnl=("closed_pnl", "sum"),
        avg_pnl=("closed_pnl", "mean"),
        win_rate=("closed_pnl", lambda x: (x > 0).mean())
    )
    .reset_index()
    .sort_values("sentiment_score")
)

# -------------------------------
# SIDE-WISE PERFORMANCE BY SENTIMENT
# -------------------------------
side_sentiment_perf = (
    df_valid.groupby(["classification", "side"])
    .agg(
        trades=("closed_pnl", "size"),
        total_pnl=("closed_pnl", "sum"),
        avg_pnl=("closed_pnl", "mean"),
        win_rate=("closed_pnl", lambda x: (x > 0).mean())
    )
    .reset_index()
    .sort_values(["classification", "total_pnl"], ascending=[True, False])
)

# -------------------------------
# TOP ACCOUNTS
# -------------------------------
top_accounts = (
    df.groupby("account")
    .agg(
        trades=("closed_pnl", "size"),
        total_pnl=("closed_pnl", "sum"),
        avg_pnl=("closed_pnl", "mean"),
        win_rate=("closed_pnl", lambda x: (x > 0).mean())
    )
    .reset_index()
    .sort_values("total_pnl", ascending=False)
    .head(20)
)

# -------------------------------
# SAVE OUTPUTS
# -------------------------------
overall_summary.to_csv("outputs/tables/overall_summary.csv", index=False)
sentiment_perf.to_csv("outputs/tables/sentiment_performance.csv", index=False)
score_perf.to_csv("outputs/tables/sentiment_score_performance.csv", index=False)
side_sentiment_perf.to_csv("outputs/tables/side_sentiment_performance.csv", index=False)
top_accounts.to_csv("outputs/tables/top_accounts.csv", index=False)

# -------------------------------
# PRINT KEY INSIGHTS
# -------------------------------
print("\nOVERALL SUMMARY")
print(overall_summary.to_string(index=False))

print("\nSENTIMENT PERFORMANCE")
print(sentiment_perf.to_string(index=False))

print("\nSENTIMENT SCORE PERFORMANCE")
print(score_perf.to_string(index=False))

print("\nSIDE + SENTIMENT PERFORMANCE")
print(side_sentiment_perf.to_string(index=False))

print("\nTOP ACCOUNTS")
print(top_accounts.to_string(index=False))