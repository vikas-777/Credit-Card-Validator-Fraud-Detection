# src/validator.py
import pandas as pd

def luhn_check(card_number: str) -> bool:
    digits = [int(ch) for ch in card_number if ch.isdigit()]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def detect_issuer(card_number: str) -> str:
    s = card_number
    if s.startswith("4"):
        return "Visa"
    if s[:2] in ("51","52","53","54","55"):
        return "MasterCard"
    if s.startswith(("34","37")):
        return "American Express"
    if s.startswith("6011") or s.startswith("65"):
        return "Discover"
    return "Unknown"

def validate_dataframe(df: pd.DataFrame, card_col: str = "card_number") -> pd.DataFrame:
    df = df.copy()
    df[card_col] = df[card_col].astype(str).fillna("")
    df["is_valid"] = df[card_col].apply(luhn_check)
    df["issuer"] = df[card_col].apply(detect_issuer)
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="CSV file path")
    args = parser.parse_args()
    if args.file:
        df = pd.read_csv(args.file)
        out = validate_dataframe(df)
        out.to_csv("results/validated.csv", index=False)
        print("Saved results/validated.csv")
