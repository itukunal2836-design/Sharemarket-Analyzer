# features.py
import pandas as pd
import numpy as np

def compute_features(df, include_target=True):
    """
    df: DataFrame must contain 'Open','High','Low','Close','Volume' (index = Date)
    include_target: if True create 'Target' = (next-day close > today close).astype(int)
    """
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    # RSI (14)
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / (avg_loss + 1e-8)
    df['RSI_14'] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    # Bollinger Bands (20)
    df['BB_mid'] = df['Close'].rolling(window=20).mean()
    df['BB_std'] = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_mid'] + 2 * df['BB_std']
    df['BB_lower'] = df['BB_mid'] - 2 * df['BB_std']
    df['BB_width'] = (df['BB_upper'] - df['BB_lower']) / (df['BB_mid'] + 1e-8)
    # volume feature
    df['Vol_Change'] = df['Volume'].pct_change()
    if include_target:
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df = df.dropna()
    else:
        # keep all rows (may have NaNs from indicator warm-up)
        df = df.dropna()
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    df = pd.read_csv(args.csv, index_col=0, parse_dates=True)
    feat = compute_features(df)
    if args.out:
        feat.to_csv(args.out)
        print("Saved features to", args.out)
    else:
        print(feat.tail())
