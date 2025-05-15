import pandas as pd

# Load dataset
df = pd.read_csv("data/sales_train_validation.csv")

# Get unique item IDs
unique_items = df['item_id'].unique()

print(f"Total unique products: {len(unique_items)}")
print("Example products:")
print(unique_items[:20])  # Print first 20 item IDs
