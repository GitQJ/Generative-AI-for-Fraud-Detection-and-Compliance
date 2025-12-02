#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 22:10:29 2025

@author: quentinjonneaux
"""

import pandas as pd
import numpy as np
import datetime
import random

# --- Configuration ---
NUM_TRANSACTIONS = 20000
FRAUD_RATE = 0.015  # 1.5% fraud
START_DATE = datetime.datetime(2024, 1, 1, 0, 0, 0)
END_DATE = datetime.datetime(2025, 11, 28, 23, 59, 59) # Today's date

# --- Data Lists ---
MERCHANT_CATEGORIES = {
    'Groceries': {'names': ['SuperMart', 'FreshFoods', 'DailyNeeds'], 'normal_weight': 0.2, 'fraud_weight': 0.05},
    'Restaurants': {'names': ['EatWell Diner', 'CafeLuxe', 'BurgerJoint'], 'normal_weight': 0.15, 'fraud_weight': 0.05},
    'Online Retail': {'names': ['WebShopX', 'GlobalMarket', 'E-Boutique'], 'normal_weight': 0.2, 'fraud_weight': 0.3}, # Higher for fraud
    'Travel': {'names': ['FlyAway Airlines', 'HotelVista', 'TravelGo'], 'normal_weight': 0.08, 'fraud_weight': 0.1},
    'Utilities': {'names': ['PowerCo', 'WaterWorks', 'InternetNet'], 'normal_weight': 0.07, 'fraud_weight': 0.01},
    'Entertainment': {'names': ['CinemaWorld', 'GameZone', 'ConcertLive'], 'normal_weight': 0.1, 'fraud_weight': 0.08},
    'Fuel': {'names': ['QuickGas', 'FuelUp'], 'normal_weight': 0.05, 'fraud_weight': 0.02},
    'Electronics': {'names': ['TechGadgets', 'ElectroHub'], 'normal_weight': 0.05, 'fraud_weight': 0.1},
    'Services': {'names': ['CleanPro', 'FixItAll'], 'normal_weight': 0.05, 'fraud_weight': 0.03},
    'Gambling': {'names': ['BetNow', 'LuckySpin Casino'], 'normal_weight': 0.01, 'fraud_weight': 0.25}, # Significantly higher for fraud
    'Subscription': {'names': ['StreamFlix', 'CloudService'], 'normal_weight': 0.04, 'fraud_weight': 0.01}
}

CARD_TYPES = ['Visa', 'Mastercard', 'Amex']
CURRENCY = 'EUR'

# Locations: (City, Country, Latitude, Longitude)
PRIMARY_LOCATIONS = [
    ('Dublin', 'Ireland', 53.3498, -6.2603),
    ('London', 'UK', 51.5074, -0.1278),
    ('Paris', 'France', 48.8566, 2.3522),
    ('Berlin', 'Germany', 52.5200, 13.4050),
    ('Rome', 'Italy', 41.9028, 12.4964)
]

SECONDARY_LOCATIONS = [ # More distant/unusual locations
    ('New York', 'USA', 40.7128, -74.0060),
    ('Tokyo', 'Japan', 35.6895, 139.6917),
    ('Sydney', 'Australia', -33.8688, 151.2093),
    ('Lagos', 'Nigeria', 6.5244, 3.3792),
    ('Ho Chi Minh City', 'Vietnam', 10.8231, 106.6297),
    ('Online', 'Global', 0.0, 0.0) # Placeholder for purely online transactions
]

# --- Helper Functions ---
def generate_random_timestamp(start, end):
    """Generates a random datetime object between start and end."""
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_amount(is_fraud):
    """Generates transaction amount based on whether it's fraudulent or not."""
    if is_fraud:
        # Higher amounts for fraud, more spread out, minimum 50 EUR
        return round(max(50, np.random.lognormal(mean=6, sigma=1.5)), 2)
    else:
        # Typical amounts, mostly smaller, minimum 1 EUR
        return round(max(1, np.random.lognormal(mean=2.5, sigma=0.8)), 2)

def choose_merchant_category(is_fraud):
    """Chooses a merchant category with different probabilities for fraud vs. legitimate."""
    if is_fraud:
        weights = [cat['fraud_weight'] for cat in MERCHANT_CATEGORIES.values()]
    else:
        weights = [cat['normal_weight'] for cat in MERCHANT_CATEGORIES.values()]
    
    # Normalize weights
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]

    return random.choices(list(MERCHANT_CATEGORIES.keys()), weights=normalized_weights, k=1)[0]

def choose_location(is_fraud):
    """Chooses a transaction location with different probabilities for fraud vs. legitimate."""
    if is_fraud:
        # 10% chance from primary, 90% from secondary for fraudulent transactions
        loc_choices = PRIMARY_LOCATIONS + SECONDARY_LOCATIONS
        raw_weights = [10/len(PRIMARY_LOCATIONS)] * len(PRIMARY_LOCATIONS) + \
                      [90/len(SECONDARY_LOCATIONS)] * len(SECONDARY_LOCATIONS)
    else:
        # 95% chance from primary, 5% from secondary for legitimate transactions
        loc_choices = PRIMARY_LOCATIONS + SECONDARY_LOCATIONS
        raw_weights = [95/len(PRIMARY_LOCATIONS)] * len(PRIMARY_LOCATIONS) + \
                      [5/len(SECONDARY_LOCATIONS)] * len(SECONDARY_LOCATIONS)
    
    # Normalize weights
    total_weight = sum(raw_weights)
    normalized_weights = [w / total_weight for w in raw_weights]

    return random.choices(loc_choices, weights=normalized_weights, k=1)[0]

# --- Data Generation ---
data = []
for i in range(NUM_TRANSACTIONS):
    is_fraud = random.random() < FRAUD_RATE

    timestamp = generate_random_timestamp(START_DATE, END_DATE)
    amount = generate_amount(is_fraud)
    currency = CURRENCY
    card_type = random.choice(CARD_TYPES)

    category = choose_merchant_category(is_fraud)
    # Add a random number to merchant name for variety
    merchant_name = random.choice(MERCHANT_CATEGORIES[category]['names']) + f"_{random.randint(100,999)}" 

    city, country, lat, lon = choose_location(is_fraud)

    # Introduce some "unusual hour" fraud for a subset of fraudulent transactions
    if is_fraud and random.random() < 0.3: # 30% of fraudulent transactions occur at unusual hours
        hour = random.choice([0, 1, 2, 3, 4, 5, 22, 23]) # Late night/early morning hours
        timestamp = timestamp.replace(hour=hour, minute=random.randint(0,59), second=random.randint(0,59))

    data.append({
        'transaction_id': i + 1,
        'timestamp': timestamp,
        'amount': amount,
        'currency': currency,
        'merchant_name': merchant_name,
        'merchant_category': category,
        'card_type': card_type,
        'location_city': city,
        'location_country': country,
        'latitude': lat,
        'longitude': lon,
        'is_fraud': int(is_fraud) # Convert boolean to integer (0 or 1)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Ensure transaction_id is unique and sequential (already handled, but good to confirm)
df['transaction_id'] = range(1, len(df) + 1)

# Sort by timestamp for a more realistic time-series dataset
df = df.sort_values(by='timestamp').reset_index(drop=True)

# --- Output to CSV ---
file_path = "financial_transactions_dataset.csv"
df.to_csv(file_path, index=False)

print(f"Synthetic financial transactions dataset generated with {NUM_TRANSACTIONS} records.")
print(f"Fraudulent transactions: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)")
print(f"Dataset saved to {file_path}")
