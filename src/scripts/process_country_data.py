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
        reader = csv.DictReader(f)
        for row in reader:
            year    = row.get("year", "").strip()
            name    = row.get("full_name", "").strip()
            country = row.get("country_of_citizenship", "").strip()

            # Normalize to uppercase and map to True/False/None
            sm = row.get("self_made", "").strip().upper()
            if sm == "TRUE":
                self_made = True
            elif sm == "FALSE":
                self_made = False
            else:
                self_made = None  # will become JSON null

            if year and name and country:
                records.append({
                    "year": year,
                    "full_name": name,
                    "country_of_citizenship": country,
                    "self_made": self_made
                })

    os.makedirs(out_dir, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(records)} records to {json_path}")

if __name__ == "__main__":
    main()
