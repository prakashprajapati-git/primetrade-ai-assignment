# Primetrade.ai Assignment

## Relationship Between Trader Performance and Market Sentiment

## Objective

This project explores the relationship between trader performance and Bitcoin market sentiment using:

- Historical Hyperliquid trader data
- Bitcoin Fear/Greed sentiment data

The goal is to identify whether market sentiment influences trader profitability, win rate, and trading behavior.

## Note

Datasets are not included in this repository due to size constraints.  
Please place the raw datasets inside `data/raw/` before running the scripts.

## Datasets Used

### 1. Historical Trader Data

Columns available:

- Account
- Coin
- Execution Price
- Size Tokens
- Size USD
- Side
- Timestamp IST
- Start Position
- Direction
- Closed PnL
- Transaction Hash
- Order ID
- Crossed
- Fee
- Trade ID
- Timestamp

### 2. Fear/Greed Index Data

Columns available:

- Timestamp
- Value
- Classification
- Date

## Approach

### 1. Data Cleaning

- Standardized all column names
- Converted timestamps to datetime format
- Converted numeric fields to proper numeric types
- Removed invalid rows with missing critical values

### 2. Feature Engineering

- Merged trade data with daily sentiment data using trade date
- Created:
  - profit flag
  - absolute PnL
  - size category
  - sentiment score mapping

### 3. Analysis

- Computed overall trading performance
- Compared average PnL, win rate, and total PnL across sentiment regimes
- Analyzed buy vs sell behavior by sentiment
- Identified top-performing accounts

## Key Findings

- Total trades: 79,225
- Unique accounts: 32
- Total closed PnL: 5.68M
- Average closed PnL per trade: 71.68
- Median closed PnL per trade: 0.00
- Win rate: 42.24%

### Sentiment-based insights

- Extreme Greed produced the highest average PnL per trade (~205.8) and the highest win rate (~55.3%), indicating stronger performance in bullish market conditions.
- Fear also generated high total PnL (~1.78M), but with a lower win rate (~38.2%), suggesting profitability driven by fewer large winning trades.
- Extreme Fear had the weakest performance (~1.89 average PnL, ~29.3% win rate), indicating poor trading outcomes in highly bearish sentiment.

### Side-based insights

- Sell trades significantly outperform buy trades during Extreme Fear, while buy trades often result in losses, suggesting traders struggle with catching falling markets.
- In contrast, sell trades dominate profitability in Extreme Greed, indicating stronger trend-following or exit strategies.

### Account-level insight

- A small number of accounts contributed a large share of total realized PnL.
- The top accounts were able to maintain much higher absolute profitability than the rest.

## Data Quality Note

Some trades did not map cleanly to a sentiment label and were excluded from sentiment-only summaries. This likely reflects timestamp alignment differences or missing sentiment coverage for certain trade dates.

## Files Produced

- `data/processed/historical_cleaned.csv`
- `data/processed/fear_greed_cleaned.csv`
- `data/processed/merged_data.csv`
- `outputs/tables/overall_summary.csv`
- `outputs/tables/sentiment_performance.csv`
- `outputs/tables/sentiment_score_performance.csv`
- `outputs/tables/side_sentiment_performance.csv`
- `outputs/tables/top_accounts.csv`
- `outputs/figures/avg_pnl_by_sentiment.png`
- `outputs/figures/win_rate_by_sentiment.png`
- `outputs/figures/total_pnl_by_sentiment.png`
- `outputs/figures/avg_pnl_side_sentiment.png`
- `outputs/figures/top_10_accounts.png`

## Conclusion

The analysis demonstrates a clear relationship between market sentiment and trader performance. Profitability is highest during optimistic sentiment regimes, particularly Extreme Greed, where both win rate and average returns peak.

Conversely, bearish conditions such as Extreme Fear lead to significantly weaker performance, especially for long (buy) positions.

Additionally, the results highlight that a small group of traders contributes disproportionately to total profits, indicating strong skill variance across participants.

These findings suggest that incorporating sentiment signals into trading strategies could improve decision-making, particularly in timing entries and exits.

## Limitations

- Some trades could not be mapped to sentiment due to date mismatches.
- The analysis is based on historical data and does not guarantee future performance.

## Future Work

- Build a predictive model to forecast trader profitability based on sentiment and trade features.
- Explore account-level behavior over time to identify consistent trader archetypes.
- Use intraday sentiment alignment if higher-frequency sentiment data becomes available.

## How to Run

1. Put the raw datasets in `data/raw/`
2. Run the scripts in order:
   - `python scripts/01_check_data.py`
   - `python scripts/02_data_cleaning.py`
   - `python scripts/03_feature_engineering.py`
   - `python scripts/04_analysis.py`
   - `python scripts/05_visualization.py`
3. Review the outputs in `outputs/`
