import pandas as pd
import re
import json

# Load raw data
input_path = '../routes/_data/all_billionaires_1997_2024.csv'
output_path = '../routes/_data/country_billionaires.json'

# --- Load DataFrame ---
df = pd.read_csv(input_path)

# --- Clean "country_of_citizenship" ---
df['country_of_citizenship'] = df['country_of_citizenship'].fillna('Unknown').str.strip()

# Optional: unify synonyms or alternate spellings
country_corrections = {
    'United States': 'USA',
    'United Kingdom': 'UK',
    'Russian Federation': 'Russia',
    'Korea, South': 'South Korea'
}
df['country_of_citizenship'] = df['country_of_citizenship'].replace(country_corrections)

# --- Clean "year" ---
df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

# --- Clean "self_made" ---
def parse_self_made(val):
    if isinstance(val, str):
        val = val.strip().lower()
        if 'true' in val or 'self' in val:
            return 1
        elif 'false' in val or 'inher' in val:
            return 0
    elif val is True:
        return 1
    elif val is False:
        return 0
    return pd.NA

df['self_made'] = df['self_made'].apply(parse_self_made)

# --- Clean "net_worth" ---
def parse_net_worth(val):
    if isinstance(val, str):
        match = re.match(r"([\d.]+)", val.replace(",", ""))
        if match:
            return float(match.group(1))
    elif isinstance(val, (int, float)):
        return float(val)
    return None

df['net_worth'] = df['net_worth'].apply(parse_net_worth)

# --- Clean "full_name" fields ---
df['full_name'] = df['full_name'].fillna(df['first_name'].fillna('') + ' ' + df['last_name'].fillna(''))
df['full_name'] = df['full_name'].str.title().str.strip()
df['first_name'] = df['first_name'].str.title().str.strip()
df['last_name'] = df['last_name'].str.title().str.strip()

# --- Filter out rows with missing/invalid data ---
df = df[(df['year'] > 0) & (df['country_of_citizenship'].notnull()) & (df['self_made'].notnull()) & (df['net_worth'].notnull()) & (df['full_name'].notnull()) & (df['full_name'].str.strip().ne(''))]

# --- Select and rename columns for output ---
output_df = df[['year', 'country_of_citizenship', 'self_made', 'net_worth', 'full_name']].rename(columns={
    'country_of_citizenship': 'country'
})

# --- Output as JSON ---
output_records = output_df.to_dict(orient='records')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_records, f, ensure_ascii=False, indent=2)
