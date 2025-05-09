#!/usr/bin/env python3
import os
import csv
import json

def main():
    # ←— absolute path to your CSV
    csv_path = "/Users/zhanghaiyue/Desktop/Spring 2025/ Introduction to Data Visualization/all_billionaires_1997_2024.csv"
    # JSON will be written alongside the CSV
    out_dir = os.path.dirname(csv_path)
    json_path = os.path.join(out_dir, "billionaires_country.json")

    records = []
    with open(csv_path, encoding="utf-8", newline="") as f:
        # if your file really is comma‑separated, default works; 
        # if it’s tab‑separated, change to: delimiter="\t"
        reader = csv.DictReader(f)
        for row in reader:
            year = row.get("year", "").strip()
            name = row.get("full_name", "").strip()
            country = row.get("country_of_citizenship", "").strip()
            if year and name and country:
                records.append({
                    "year": year,
                    "full_name": name,
                    "country_of_citizenship": country
                })

    # ensure output folder exists (it should)
    os.makedirs(out_dir, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(records)} records to {json_path}")

if __name__ == "__main__":
    main()
