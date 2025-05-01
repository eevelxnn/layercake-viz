import pandas as pd
import numpy as np
import json
import os

# Input and output paths
input_path = 'src/routes/_data/all_billionaires_1997_2024.csv'
output_path = 'src/routes/_data/industry_wealth.json'

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

    # Get top 10 industries by billionaire count
    industry_counts = df['business_industries'].value_counts().head(10).index.tolist()

    # Filter to top industries
    df_top_industries = df[df['business_industries'].isin(industry_counts)]

    # Group by year, industry, and self-made status
    industry_data = []
    
    for year in sorted(df['year'].unique()):
        year_df = df_top_industries[df_top_industries['year'] == year]
        
        # All billionaires
        all_data = {
            'year': int(year),
            'filter': 'all'
        }
        
        # Self-made billionaires
        self_made_data = {
            'year': int(year),
            'filter': 'self-made'
        }
        
        # Inherited billionaires
        inherited_data = {
            'year': int(year),
            'filter': 'inherited'
        }
        
        for industry in industry_counts:
            industry_df = year_df[year_df['business_industries'] == industry]
            
            # Calculate total wealth for all billionaires in this industry
            all_data[industry] = round(industry_df['net_worth_clean'].sum(), 2)
            
            # Calculate total wealth for self-made billionaires
            self_made_wealth = industry_df[industry_df['self_made'] == True]['net_worth_clean'].sum()
            self_made_data[industry] = round(self_made_wealth, 2)
            
            # Calculate total wealth for inherited billionaires
            inherited_wealth = industry_df[industry_df['self_made'] == False]['net_worth_clean'].sum()
            inherited_data[industry] = round(inherited_wealth, 2)
        
        industry_data.append(all_data)
        industry_data.append(self_made_data)
        industry_data.append(inherited_data)

    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(industry_data, f, indent=2)
    
    print(f"✅ Processed industry data saved to: {output_path}")

    # Print columns for debugging
    print(df.columns)

if __name__ == '__main__':
    main()
