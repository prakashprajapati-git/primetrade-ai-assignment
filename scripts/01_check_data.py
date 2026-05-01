import pandas as pd

hist_path = "data/raw/historical_data.csv"
fg_path = "data/raw/fear_greed_index.csv"

hist = pd.read_csv(hist_path)
fg = pd.read_csv(fg_path)

print("Historical data shape:", hist.shape)
print("Fear/Greed data shape:", fg.shape)

print("\nHistorical columns:")
print(hist.columns.tolist())

print("\nFear/Greed columns:")
print(fg.columns.tolist())

print("\nHistorical head:")
print(hist.head())

print("\nFear/Greed head:")
print(fg.head())

print("\nHistorical info:")
print(hist.info())

print("\nFear/Greed info:")
print(fg.info())