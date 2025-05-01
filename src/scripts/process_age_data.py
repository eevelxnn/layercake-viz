import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# Input and output paths
input_path = 'src/routes/_data/all_billionaires_1997_2024.csv'
output_path = 'static/billionaire_ages.json'

# Parse string like "2.3 B" into float
def parse_net_worth(value):
    if isinstance(value, str) and value.endswith("B"):
        try:
            return float(value.replace(" B", "").replace("B", ""))
        except ValueError:
            print(f"Error parsing net worth: {value}")  # Debugging statement
            return np.nan
    return np.nan

def calculate_age(birth_year, current_year):
    if pd.isna(birth_year) or birth_year == 0:
        return None
    
    # Ensure birth_year is an integer
    try:
        birth_year = int(birth_year)
        # Basic validation - if birth year is too recent or too old, it's likely an error
        if birth_year < 1850 or birth_year > current_year:
            return None
        return current_year - birth_year
    except:
        return None

def main():
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    # Load CSV
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Check first few rows
    print(df.head())
    
    # Clean net worth
    df['net_worth_clean'] = df['net_worth'].apply(parse_net_worth)

    # Normalize self_made to boolean
    df['self_made'] = df['self_made'].astype(str).str.lower().map({'true': True, 'false': False})
    
    # Convert columns to numeric
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    if 'birth_year' in df.columns:
        df['birth_year'] = pd.to_numeric(df['birth_year'], errors='coerce')
        df['age'] = df['year'] - df['birth_year']
    elif 'birth_date' in df.columns:
        df['birth_year'] = pd.to_datetime(df['birth_date'], errors='coerce').dt.year
        df['age'] = df['year'] - df['birth_year']
    else:
        print("No birth year or birth date column found in the data!")
        return

    # Check for missing birth dates
    print(f"Missing birth dates: {df['birth_year'].isna().sum()}")

    # Remove rows with missing or invalid ages
    df = df[df['age'].notnull() & (df['age'] > 0)]
    print(f"Rows after filtering: {len(df)}")  # Check how many rows are left after filtering
    
    # Round age to integer
    df['age'] = df['age'].astype(int)
    
    # Group by year, age, and self-made status
    print("Aggregating data...")
    result = []
    
    for year in sorted(df['year'].unique()):
        year_df = df[df['year'] == year]
        
        for age in sorted(year_df['age'].unique()):
            age_df = year_df[year_df['age'] == age]
            
            # Count and sum wealth for self-made
            self_made_count = len(age_df[age_df['self_made'] == True])
            self_made_wealth = age_df[age_df['self_made'] == True]['net_worth_clean'].sum()
            
            # Count and sum wealth for inherited
            inherited_count = len(age_df[age_df['self_made'] == False])
            inherited_wealth = age_df[age_df['self_made'] == False]['net_worth_clean'].sum()
            
            if self_made_count > 0 or inherited_count > 0:
                result.append({
                    'year': int(year),
                    'age': int(age),
                    'self_made_count': int(self_made_count),
                    'self_made_wealth': round(float(self_made_wealth), 2),
                    'inherited_count': int(inherited_count),
                    'inherited_wealth': round(float(inherited_wealth), 2),
                    'total_count': self_made_count + inherited_count,
                    'total_wealth': round(float(self_made_wealth + inherited_wealth), 2)
                })
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Processed age data saved to: {output_path}")
    print(f"Total records: {len(result)}")
    
    # Print some statistics
    years = sorted(set(item['year'] for item in result))
    if years:
        print(f"Years covered: {min(years)} to {max(years)}")
    else:
        print("No years found in processed data.")
    
    age_range = [item['age'] for item in result]
    print(f"Age range: {min(age_range)} to {max(age_range)}")

if __name__ == '__main__':
    main()
