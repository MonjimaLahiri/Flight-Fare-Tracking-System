import json
from datetime import datetime, timedelta
from google_scraper import scrape_google
from mmt_scraper import scrape_mmt
from db_utils import save_to_db

# Ask user for input
source_input = input("Enter source airport code (e.g., HYD): ").strip().upper()
destination_input = input("Enter destination airport code (e.g., DEL): ").strip().upper()
date_input = input("Enter preferred travel date (YYYY-MM-DD): ").strip()

try:
    preferred_date = datetime.strptime(date_input, "%Y-%m-%d").date()
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

# Load airport mapper
with open("airport_mapper.json", "r") as f:
    airport_map = json.load(f)

# Get nearby airport lists
source_airports = [source_input] + airport_map.get(source_input, [])[:2]
destination_airports = [destination_input] + airport_map.get(destination_input, [])[:2]

# Prepare date range ±7 days
date_range = [preferred_date + timedelta(days=i) for i in range(-7, 8)]
#data_range = [preferred_date]

print(f"\n Scraping all combinations from {source_airports} to {destination_airports}")
print(f" For dates from {date_range[0]} to {date_range[-1]}\n")

# Begin scraping loop
for src in source_airports:
    for dest in destination_airports:
        if src == dest:
            continue  # skip same airport combos

        for travel_date in date_range[:1]:
            print(f"  {src} → {dest} on {travel_date}")

            g_price, g_airline = scrape_google(src, dest, travel_date)
            m_price, m_airline = scrape_mmt(src, dest, travel_date)

            print(f"  Google: ₹{g_price} | {g_airline}")
            print(f"  MMT:    ₹{m_price} | {m_airline}")

            # Skip if both fail
            if g_price is None and m_price is None:
                print("  Skipping: No data from either source.\n")
                continue

            # Choose cheaper
            if g_price is not None and (m_price is None or g_price <= m_price):
                best = (src, dest, travel_date, g_airline, g_price, "Google")
            else:
                best = (src, dest, travel_date, m_airline, m_price, "MMT")

            # Save to DB
            save_to_db([best])
            print(" Saved cheapest fare to DB.\n")
