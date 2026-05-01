import pandas as pd

# Load cleaned data
hist = pd.read_csv("data/processed/historical_cleaned.csv")
fg = pd.read_csv("data/processed/fear_greed_cleaned.csv")

# -------------------------------
# PREPARE TIME FEATURES
# -------------------------------

# Convert datetime again (safety)
hist["timestamp_ist"] = pd.to_datetime(hist["timestamp_ist"])
fg["date"] = pd.to_datetime(fg["date"])

# Extract date from trades
hist["trade_date"] = hist["timestamp_ist"].dt.date
fg["date"] = fg["date"].dt.date

# -------------------------------
# MERGE DATASETS
# -------------------------------

merged = pd.merge(
    hist,
    fg,
    left_on="trade_date",
    right_on="date",
    how="left"
)

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------

# Profitability flag
merged["is_profit"] = merged["closed_pnl"] > 0

# Absolute PnL
merged["abs_pnl"] = merged["closed_pnl"].abs()

# Trade size category
merged["size_category"] = pd.qcut(
    merged["size_usd"],
    q=4,
    labels=["small", "medium", "large", "very_large"]
)

# Encode sentiment (important for analysis)
sentiment_map = {
    "extreme fear": 0,
    "fear": 1,
    "neutral": 2,
    "greed": 3,
    "extreme greed": 4
}

merged["sentiment_score"] = merged["classification"].map(sentiment_map)

# -------------------------------
# SAVE
# -------------------------------

merged.to_csv("data/processed/merged_data.csv", index=False)

print("Feature engineering completed.")
print("Merged dataset shape:", merged.shape)
print("\nSample:")
print(merged.head())