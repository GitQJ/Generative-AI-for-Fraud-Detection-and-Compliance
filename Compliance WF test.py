#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 20:38:05 2025

@author: quentinjonneaux
"""

import datetime

def predict_fraud(transaction):
    """
    A mock fraud detection model.
    In a real-world scenario, this would be a machine learning model.
    For this example, we'll use a simple rule-based approach.
    """
    # Rule: Flag transactions with an amount greater than $500
    if transaction['amount'] > 500:
        return 'fraudulent'
    return 'normal'

def compliance_workflow(transactions):
    """
    The compliance workflow that checks each transaction.
    """
    flagged_transactions = []
    for transaction in transactions:
        prediction = predict_fraud(transaction)
        if prediction == 'fraudulent':
            transaction['status'] = 'flagged'
            transaction['action_taken'] = 'Flagged for Manual Review'
            flagged_transactions.append(transaction)
    return flagged_transactions

def generate_report(flagged_transactions):
    """
    Generates a report of flagged transactions.
    """
    print("--- Fraud Detection Report ---")
    print(f"Report generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTotal flagged transactions: {len(flagged_transactions)}")
    print("---------------------------------")

    if not flagged_transactions:
        print("\nNo suspicious transactions detected.")
    else:
        print("\nFlagged Transactions:\n")
        for transaction in flagged_transactions:
            print(f"  Transaction ID: {transaction['transaction_id']}")
            print(f"  Timestamp: {transaction['timestamp']}")
            print(f"  Amount: {transaction['amount']} {transaction['currency']}")
            print(f"  Merchant: {transaction['merchant_name']}")
            print(f"  Action Taken: {transaction['action_taken']}")
            print("  --------------------")

# Sample transactions for demonstration
sample_transactions = [
    {'transaction_id': 'txn_1', 'timestamp': '2025-11-20T10:30:00', 'amount': 150.75, 'currency': 'USD', 'merchant_name': 'Gadget World'},
    {'transaction_id': 'txn_2', 'timestamp': '2025-11-20T10:32:00', 'amount': 800.00, 'currency': 'GBP', 'merchant_name': 'FlyAway'},
    {'transaction_id': 'txn_3', 'timestamp': '2025-11-20T10:35:00', 'amount': 250.20, 'currency': 'USD', 'merchant_name': 'Tech Central'},
    {'transaction_id': 'txn_4', 'timestamp': '2025-11-20T10:40:00', 'amount': 950.00, 'currency': 'USD', 'merchant_name': 'Holiday Planners'},
    {'transaction_id': 'txn_5', 'timestamp': '2025-11-20T10:45:00', 'amount': 120.90, 'currency': 'GBP', 'merchant_name': 'Style Central'},
]

# --- Execute the Workflow ---
flagged = compliance_workflow(sample_transactions)

# --- Generate the Report ---
generate_report(flagged)

