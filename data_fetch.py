# data_fetch.py
import yfinance as yf
import os
import argparse
from datetime import date

def fetch_and_save(ticker, start=None, end=None, outdir='data'):
    start = start or '2015-01-01'
    end = end or date.today().isoformat()
    os.makedirs(outdir, exist_ok=True)
    print(f"Downloading {ticker} from {start} to {end} ...")
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}")
    path = os.path.join(outdir, f"{ticker}.csv")
    df.to_csv(path)
    print(f"Saved {len(df)} rows to {path}")
    return path

if __name__ == "__main__":
    import traceback
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True, help="Ticker symbol, e.g. AAPL")
    parser.add_argument("--start", required=False, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=False, help="End date YYYY-MM-DD")
    parser.add_argument("--outdir", default="data")
    args = parser.parse_args()
    try:
        fetch_and_save(args.ticker, args.start, args.end, args.outdir)
    except Exception as e:
        print("\n--- ERROR ---")
        traceback.print_exc()
        print("\nIf you see 'No data returned', check ticker and date range.")
