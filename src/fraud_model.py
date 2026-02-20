# src/fraud_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

os.makedirs("results", exist_ok=True)

def prepare_features(df: pd.DataFrame):
    df = df.copy()
    if "transaction_time" in df.columns:
        df["transaction_time"] = pd.to_datetime(df["transaction_time"], errors="coerce")
        df["hour"] = df["transaction_time"].dt.hour.fillna(0).astype(int)
        df["dayofweek"] = df["transaction_time"].dt.dayofweek.fillna(0).astype(int)
    else:
        df["hour"] = 0
        df["dayofweek"] = 0
    features = ["transaction_amount", "hour", "dayofweek", "issuer", "country", "merchant"]
    for c in features:
        if c not in df.columns:
            df[c] = 0 if c in ("transaction_amount","hour","dayofweek") else "Unknown"
    X = df[features]
    y = df["fraud"].astype(int) if "fraud" in df.columns else pd.Series([0]*len(df))
    return X, y

def train_simple_model(df: pd.DataFrame):
    X, y = prepare_features(df)
    numeric = ["transaction_amount", "hour", "dayofweek"]
    categorical = ["issuer", "country", "merchant"]
    pre = ColumnTransformer([
        ("num", "passthrough", numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
    ])
    pipe = Pipeline([("pre", pre), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if y.nunique()>1 else None)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    report = classification_report(y_test, preds, output_dict=True, zero_division=0)
    joblib.dump(pipe, "results/best_model.pkl")
    pd.DataFrame(report).transpose().to_csv("results/model_metrics.csv")
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        df = pd.read_csv(sys.argv[1])
        r = train_simple_model(df)
        print("Saved model and metrics to results/")
