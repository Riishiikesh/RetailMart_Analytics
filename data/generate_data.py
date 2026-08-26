"""
Script to generate sample data for RetailMart case study
Run this script to generate sales_transactions, sales_items, vouchers, voucher_redemptions, and returns
"""

import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_TRANSACTIONS = 5000
NUM_VOUCHERS = 100
NUM_RETURNS = 500
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

STORES = [1, 2, 3, 4, 5]
PAYMENT_METHODS = ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Wallet']
RETURN_REASONS = ['Defective', 'Wrong Size', 'Not as Described', 'Changed Mind', 'Better Price Elsewhere']
VOUCHER_TYPES = ['Percentage', 'Flat']

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_sales_transactions():
    transactions = []
    for i in range(1, NUM_TRANSACTIONS + 1):
        trans_date = random_date(START_DATE, END_DATE)
        transactions.append({
            'transaction_id': i,
            'customer_id': random.randint(1, 50) if random.random() > 0.2 else None,  # 20% guest checkout
            'store_id': random.choice(STORES),
            'transaction_date': trans_date.strftime('%Y-%m-%d'),
            'transaction_time': f"{random.randint(9, 21):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
            'payment_method': random.choice(PAYMENT_METHODS),
            'total_amount': 0,  # Will be calculated
            'discount_amount': 0,
            'tax_amount': 0,
            'net_amount': 0
        })
    return transactions

def generate_sales_items(transactions):
    items = []
    item_id = 1
    for trans in transactions:
        num_items = random.randint(1, 5)
        trans_total = 0
        used_products = set()

        for _ in range(num_items):
            product_id = random.randint(1, 50)
            while product_id in used_products:
                product_id = random.randint(1, 50)
            used_products.add(product_id)

            quantity = random.randint(1, 3)
            # Price ranges based on product categories
            base_prices = [2499, 299, 1299, 599, 1499, 1999, 450, 180, 520, 899,
                          1299, 649, 249, 399, 349, 799, 1499, 199, 149, 99,
                          399, 999, 699, 499, 2499, 899, 1299, 799, 1499, 699,
                          3499, 599, 1299, 899, 280, 320, 1899, 999, 549, 199,
                          899, 699, 79, 199, 1299, 449, 1799, 1999, 2499, 1999]
            unit_price = base_prices[product_id - 1]
            line_total = unit_price * quantity
            trans_total += line_total

            items.append({
                'item_id': item_id,
                'transaction_id': trans['transaction_id'],
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total
            })
            item_id += 1

        # Update transaction totals
        discount = round(trans_total * random.uniform(0, 0.15), 2) if random.random() > 0.6 else 0
        tax = round((trans_total - discount) * 0.18, 2)
        trans['total_amount'] = trans_total
        trans['discount_amount'] = discount
        trans['tax_amount'] = tax
        trans['net_amount'] = round(trans_total - discount + tax, 2)

    return items

def generate_vouchers():
    vouchers = []
    for i in range(1, NUM_VOUCHERS + 1):
        voucher_type = random.choice(VOUCHER_TYPES)
        start = random_date(START_DATE, END_DATE)
        vouchers.append({
            'voucher_id': i,
            'voucher_code': f"RETAIL{i:04d}",
            'voucher_type': voucher_type,
            'discount_value': random.choice([5, 10, 15, 20]) if voucher_type == 'Percentage' else random.choice([50, 100, 200, 500]),
            'min_purchase_amount': random.choice([500, 1000, 2000, 5000]),
            'max_discount_amount': random.choice([100, 200, 500, 1000]) if voucher_type == 'Percentage' else None,
            'valid_from': start.strftime('%Y-%m-%d'),
            'valid_to': (start + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d'),
            'is_active': 1 if random.random() > 0.2 else 0
        })
    return vouchers

def generate_voucher_redemptions(vouchers, transactions):
    redemptions = []
    redemption_id = 1
    eligible_transactions = [t for t in transactions if t['discount_amount'] > 0 and t['customer_id']]

    for _ in range(300):
        if not eligible_transactions:
            break
        trans = random.choice(eligible_transactions)
        voucher = random.choice(vouchers)

        redemptions.append({
            'redemption_id': redemption_id,
            'voucher_id': voucher['voucher_id'],
            'transaction_id': trans['transaction_id'],
            'customer_id': trans['customer_id'],
            'redemption_date': trans['transaction_date'],
            'discount_applied': min(trans['discount_amount'], voucher['max_discount_amount'] or trans['discount_amount'])
        })
        eligible_transactions.remove(trans)
        redemption_id += 1

    return redemptions

def generate_returns(transactions, items):
    returns = []
    # Group items by transaction
    trans_items = {}
    for item in items:
        tid = item['transaction_id']
        if tid not in trans_items:
            trans_items[tid] = []
        trans_items[tid].append(item)

    eligible_trans = [t for t in transactions if t['customer_id']]
    selected_trans = random.sample(eligible_trans, min(NUM_RETURNS, len(eligible_trans)))

    for i, trans in enumerate(selected_trans, 1):
        trans_date = datetime.strptime(trans['transaction_date'], '%Y-%m-%d')
        return_date = trans_date + timedelta(days=random.randint(1, 30))

        if return_date > END_DATE:
            return_date = END_DATE

        if trans['transaction_id'] in trans_items:
            item = random.choice(trans_items[trans['transaction_id']])
            return_qty = random.randint(1, item['quantity'])

            returns.append({
                'return_id': i,
                'transaction_id': trans['transaction_id'],
                'item_id': item['item_id'],
                'customer_id': trans['customer_id'],
                'product_id': item['product_id'],
                'return_date': return_date.strftime('%Y-%m-%d'),
                'return_quantity': return_qty,
                'return_reason': random.choice(RETURN_REASONS),
                'refund_amount': round(item['unit_price'] * return_qty, 2),
                'refund_status': random.choice(['Processed', 'Processed', 'Processed', 'Pending'])
            })

    return returns

def write_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {filename} with {len(data)} records")

if __name__ == "__main__":
    print("Generating sample data for RetailMart...")

    # Generate data
    transactions = generate_sales_transactions()
    items = generate_sales_items(transactions)
    vouchers = generate_vouchers()
    redemptions = generate_voucher_redemptions(vouchers, transactions)
    returns = generate_returns(transactions, items)

    # Write CSV files
    write_csv('sales_transactions.csv', transactions,
              ['transaction_id', 'customer_id', 'store_id', 'transaction_date', 'transaction_time',
               'payment_method', 'total_amount', 'discount_amount', 'tax_amount', 'net_amount'])

    write_csv('sales_items.csv', items,
              ['item_id', 'transaction_id', 'product_id', 'quantity', 'unit_price', 'line_total'])

    write_csv('vouchers.csv', vouchers,
              ['voucher_id', 'voucher_code', 'voucher_type', 'discount_value', 'min_purchase_amount',
               'max_discount_amount', 'valid_from', 'valid_to', 'is_active'])

    write_csv('voucher_redemptions.csv', redemptions,
              ['redemption_id', 'voucher_id', 'transaction_id', 'customer_id', 'redemption_date', 'discount_applied'])

    write_csv('returns.csv', returns,
              ['return_id', 'transaction_id', 'item_id', 'customer_id', 'product_id',
               'return_date', 'return_quantity', 'return_reason', 'refund_amount', 'refund_status'])

    print("\nData generation complete!")
