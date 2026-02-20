# src/dashboard.py
import streamlit as st
import pandas as pd
import joblib
from validator import validate_dataframe

st.title("Card Validator and Fraud Demo")

uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    if "card_number" not in df.columns:
        st.info("No card_number column found. Using synthetic demo values.")
        df = df.head(100)
        df["card_number"] = ["4111111111111111"] * len(df)
        df["fraud"] = [0]*len(df)
    validated = validate_dataframe(df)
    st.write("Validation summary")
    st.dataframe(validated[["card_number","issuer","is_valid"]].head())

    if st.button("Load model and predict"):
        try:
            model = joblib.load("results/best_model.pkl")
            X, _ = __import__("fraud_model").fraud_model.prepare_features(validated)
            preds = model.predict(X)
            validated["predicted_fraud"] = preds
            st.write(validated[["card_number","transaction_amount","issuer","predicted_fraud"]].head())
        except Exception as e:
            st.error("Model not found. Train model first.")
