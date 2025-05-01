import pandas as pd
import numpy as np
import os

# Input and output paths
input_path = '/Users/ev/Desktop/School/layercake-dataviz/src/routes/_data/all_billionaires_1997_2024.csv'
output_path = '/Users/ev/Desktop/School/layercake-dataviz/src/routes/_data/billionaires_by_year.json'

# Parse string like "2.3 B" into float
def parse_net_worth(value):
    if isinstance(value, str) and value.endswith("B"):
        try:
            return float(value.replace(" B", "").replace("B", ""))
        except ValueError:
            return np.nan
    return np.nan

def main():
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    # Load CSV
    df = pd.read_csv(input_path)

    # Clean net worth
    df['net_worth_clean'] = df['net_worth'].apply(parse_net_worth)

    # Normalize self_made to boolean
    df['self_made'] = df['self_made'].astype(str).str.lower().map({'true': True, 'false': False})

    # Group by year, name, and self-made flag, then average
    grouped = (
        df.groupby(['year', 'full_name', 'self_made'], as_index=False)
          .agg(avg_net_worth=('net_worth_clean', 'mean'))
    )

    # Round to 2 decimals
    grouped['avg_net_worth'] = grouped['avg_net_worth'].round(2)

    # Save to JSON
    grouped.to_json(output_path, orient='records', indent=2)
    print(f"✅ Processed data saved to: {output_path}")

if __name__ == '__main__':
    main()
