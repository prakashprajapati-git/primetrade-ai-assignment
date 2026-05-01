import pandas as pd

# Load data
hist = pd.read_csv("data/raw/historical_data.csv")
fg = pd.read_csv("data/raw/fear_greed_index.csv")

# -------------------------------
# STANDARDIZE COLUMN NAMES
# -------------------------------
hist.columns = hist.columns.str.strip().str.lower().str.replace(" ", "_")
fg.columns = fg.columns.str.strip().str.lower().str.replace(" ", "_")

# -------------------------------
# CLEAN HISTORICAL DATA
# -------------------------------

# Convert timestamp_ist to datetime
hist["timestamp_ist"] = pd.to_datetime(hist["timestamp_ist"], errors="coerce")

# Also convert epoch timestamp (optional but useful)
hist["timestamp"] = pd.to_datetime(hist["timestamp"], unit="ms", errors="coerce")

# Convert numeric columns (safe)
numeric_cols = [
    "execution_price",
    "size_tokens",
    "size_usd",
    "closed_pnl",
    "fee",
    "start_position"
]

for col in numeric_cols:
    if col in hist.columns:
        hist[col] = pd.to_numeric(hist[col], errors="coerce")

# Clean categorical columns
hist["side"] = hist["side"].str.lower().str.strip()
hist["direction"] = hist["direction"].str.lower().str.strip()

# Drop invalid rows (important)
hist = hist.dropna(subset=[
    "timestamp_ist",
    "execution_price",
    "size_usd",
    "side",
    "closed_pnl"
])

# -------------------------------
# CLEAN FEAR GREED DATA
# -------------------------------

fg["date"] = pd.to_datetime(fg["date"], errors="coerce")
fg["classification"] = fg["classification"].str.lower().str.strip()

# -------------------------------
# SAVE CLEAN DATA
# -------------------------------

hist.to_csv("data/processed/historical_cleaned.csv", index=False)
fg.to_csv("data/processed/fear_greed_cleaned.csv", index=False)

print("Cleaning completed.")
print("Cleaned historical shape:", hist.shape)
print("Cleaned fear/greed shape:", fg.shape)