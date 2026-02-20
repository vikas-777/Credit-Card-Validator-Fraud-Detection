import csv
import random
from datetime import datetime, timedelta

# Fix random seed for reproducibility
random.seed(42)

# Issuer prefixes and names
issuers = [
    ("4", "Visa"),
    ("51", "MasterCard"),
    ("34", "American Express"),
    ("6011", "Discover")
]

def generate_card(prefix, length=16):
    """Generate a synthetic card number with prefix (not full Luhn check for simplicity)."""
    body = "".join(random.choice("0123456789") for _ in range(length - len(prefix)))
    return prefix + body

# Generate dataset
rows = []
start_date = datetime(2025, 1, 1)

for i in range(100000):  # 1 lakh records
    prefix, issuer = random.choice(issuers)
    card_number = generate_card(prefix)
    amount = round(random.uniform(1, 1000), 2)
    country = random.choice(["US", "UK", "IN", "CA", "AU"])
    merchant = random.choice(["Amazon", "Walmart", "Flipkart", "Target", "Starbucks", "eBay"])
    tx_time = start_date + timedelta(minutes=i)
    fraud = random.choice([0, 0, 0, 1])  # ~25% fraud rate
    rows.append([card_number, amount, country, merchant, tx_time.strftime("%Y-%m-%d %H:%M:%S"), fraud])

# Save to CSV
with open("sample_cards_100k.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["card_number", "transaction_amount", "country", "merchant", "transaction_time", "fraud"])
    writer.writerows(rows)

print("✅ Generated sample_cards_100k.csv with 100,000 records")
