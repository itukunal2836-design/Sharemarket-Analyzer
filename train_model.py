# train_model.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

from features import compute_features

def train_from_csv(csv_path, model_dir='models', n_estimators=100):
    os.makedirs(model_dir, exist_ok=True)
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    df_feat = compute_features(df, include_target=True)
    # Features used (you can tune this list)
    feature_cols = ['Return','SMA_5','SMA_10','EMA_10','RSI_14','MACD','MACD_signal','BB_width','Vol_Change','Volume']
    # drop rows that might still have NaNs
    df_feat = df_feat.dropna(subset=feature_cols + ['Target'])
    X = df_feat[feature_cols]
    y = df_feat['Target']
    # time-based split (no shuffle)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    # scaling
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42, n_jobs=-1)
    clf.fit(X_train_s, y_train)
    preds = clf.predict(X_test_s)
    acc = accuracy_score(y_test, preds)
    print("Accuracy on test set:", acc)
    print("Classification report:")
    print(classification_report(y_test, preds))
    print("Confusion matrix:\n", confusion_matrix(y_test, preds))
    # save
    base = os.path.splitext(os.path.basename(csv_path))[0]
    model_path = os.path.join(model_dir, f"{base}_rf.joblib")
    scaler_path = os.path.join(model_dir, f"{base}_scaler.joblib")
    joblib.dump(clf, model_path)
    joblib.dump(scaler, scaler_path)
    print("Saved model to", model_path)
    print("Saved scaler to", scaler_path)
    return model_path, scaler_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="CSV file (downloaded OHLCV) e.g. data/AAPL.csv")
    parser.add_argument("--model_dir", default="models")
    args = parser.parse_args()
    train_from_csv(args.csv, args.model_dir)
