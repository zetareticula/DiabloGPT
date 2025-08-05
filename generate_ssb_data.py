#!/usr/bin/env python3
"""
Generate sample SSB (Star Schema Benchmark) data for testing EINSTEINAI4DB.
"""
import os
import numpy as np
import pandas as pd
from pathlib import Path

# Create data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'ssb')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_date_dimension(n=2556):
    """Generate date dimension table."""
    dates = pd.date_range('1992-01-01', periods=n, freq='D')
    
    df = pd.DataFrame({
        'd_datekey': range(1, n + 1),
        'd_date': dates.strftime('%Y-%m-%d'),
        'd_dayofweek': dates.dayofweek + 1,
        'd_month': dates.month,
        'd_year': dates.year,
        'd_yearmonthnum': dates.year * 100 + dates.month,
        'd_yearmonth': dates.strftime('%Y-%m'),
        'd_weeknuminyear': dates.isocalendar().week,
        'd_sellingseason': np.random.choice(['Spring', 'Summer', 'Fall', 'Winter'], size=n, p=[0.25, 0.25, 0.25, 0.25]),
        'd_lastdayinweekfl': (dates.dayofweek == 6).astype(int),
        'd_holidayfl': (dates.dayofweek >= 5).astype(int),  # Mark weekends as holidays
        'd_weekdayfl': (dates.dayofweek < 5).astype(int)
    })
    
    return df

def generate_part_dimension(n=200000):
    """Generate part dimension table."""
    categories = ['MFGR#1', 'MFGR#2', 'MFGR#3', 'MFGR#4', 'MFGR#5']
    brands = [f'Brand#{i+1}' for i in range(25)]
    
    df = pd.DataFrame({
        'p_partkey': range(1, n + 1),
        'p_name': [f'Part #{i}' for i in range(1, n + 1)],
        'p_mfgr': np.random.choice(categories, size=n),
        'p_category': np.random.choice(['Category1', 'Category2', 'Category3', 'Category4', 'Category5'], size=n),
        'p_brand': np.random.choice(brands, size=n),
        'p_color': np.random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White'], size=n),
        'p_type': np.random.choice(['SMALL', 'MEDIUM', 'LARGE', 'ECONOMY', 'STANDARD', 'PROMO'], size=n),
        'p_size': np.random.randint(1, 51, size=n),
        'p_container': np.random.choice(['SM CASE', 'SM BOX', 'SM PACK', 'SM PKG', 'MED BAG', 'MED BOX', 
                                        'MED PKG', 'MED PACK', 'LG CASE', 'LG BOX', 'LG PACK', 'LG PKG'], size=n)
    })
    
    return df

def generate_supplier_dimension(n=20000):
    """Generate supplier dimension table."""
    regions = ['AMERICA', 'ASIA', 'EUROPE', 'AFRICA', 'MIDDLE EAST']
    
    df = pd.DataFrame({
        's_suppkey': range(1, n + 1),
        's_name': [f'Supplier#{i}' for i in range(1, n + 1)],
        's_address': [f'Address {i}' for i in range(1, n + 1)],
        's_city': [f'City {i % 100}' for i in range(1, n + 1)],
        's_nation': [f'Nation {i % 25}' for i in range(1, n + 1)],
        's_region': np.random.choice(regions, size=n, p=[0.4, 0.3, 0.2, 0.05, 0.05]),
        's_phone': [f'Phone-{i:010d}' for i in range(1, n + 1)]
    })
    
    return df

def generate_customer_dimension(n=300000):
    """Generate customer dimension table."""
    segments = ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'HOUSEHOLD', 'MACHINERY']
    
    df = pd.DataFrame({
        'c_custkey': range(1, n + 1),
        'c_name': [f'Customer#{i}' for i in range(1, n + 1)],
        'c_address': [f'Address {i}' for i in range(1, n + 1)],
        'c_city': [f'City {i % 100}' for i in range(1, n + 1)],
        'c_nation': [f'Nation {i % 25}' for i in range(1, n + 1)],
        'c_region': np.random.choice(['AMERICA', 'ASIA', 'EUROPE', 'AFRICA', 'MIDDLE EAST'], 
                                   size=n, p=[0.4, 0.3, 0.2, 0.05, 0.05]),
        'c_phone': [f'Phone-{i:010d}' for i in range(1, n + 1)],
        'c_mktsegment': np.random.choice(segments, size=n)
    })
    
    return df

def generate_lineorder_fact(n=10000):
    """Generate lineorder fact table."""
    # Generate keys with some skew to match real-world distributions
    cust_keys = np.random.choice(range(1, 300001), size=n, replace=True)
    part_keys = np.random.choice(range(1, 200001), size=n, replace=True)
    supp_keys = np.random.choice(range(1, 20001), size=n, replace=True)
    date_keys = np.random.choice(range(1, 2557), size=n, replace=True)
    
    # Generate measures with some correlations
    quantities = np.random.randint(1, 51, size=n)
    extended_prices = np.random.uniform(1, 50000, size=n).round(2)
    discounts = np.random.uniform(0, 0.2, size=n).round(4)
    taxes = np.random.uniform(0, 0.1, size=n).round(4)
    
    df = pd.DataFrame({
        'lo_orderkey': range(1, n + 1),
        'lo_linenumber': np.tile(range(1, 6), n // 5 + 1)[:n],
        'lo_custkey': cust_keys,
        'lo_partkey': part_keys,
        'lo_suppkey': supp_keys,
        'lo_orderdate': date_keys,
        'lo_orderpriority': np.random.choice(['1-URGENT', '2-HIGH', '3-MEDIUM', '4-NOT SPECIFIED', '5-LOW'], size=n),
        'lo_shippriority': np.random.choice(['1-HIGH', '2-MEDIUM', '3-LOW'], size=n),
        'lo_quantity': quantities,
        'lo_extendedprice': extended_prices,
        'lo_ordtotalprice': (extended_prices * (1 + taxes)).round(2),
        'lo_discount': discounts,
        'lo_revenue': (extended_prices * (1 - discounts)).round(2),
        'lo_supplycost': (extended_prices * 0.7).round(2),
        'lo_tax': taxes,
        'lo_commitdate': np.random.choice(range(1, 2557), size=n, replace=True),
        'lo_shipmode': np.random.choice(['AIR', 'SHIP', 'TRUCK', 'RAIL', 'MAIL'], size=n)
    })
    
    return df

def save_to_csv(df, table_name):
    """Save DataFrame to CSV file."""
    filename = os.path.join(DATA_DIR, f'{table_name}.csv')
    df.to_csv(filename, index=False)
    print(f'Saved {len(df)} rows to {filename}')

def main():
    """Generate and save sample SSB data."""
    print("Generating SSB sample data...")
    
    # Generate and save dimension tables
    print("\nGenerating dimension tables...")
    date_df = generate_date_dimension()
    save_to_csv(date_df, 'date')
    
    part_df = generate_part_dimension()
    save_to_csv(part_df, 'part')
    
    supplier_df = generate_supplier_dimension()
    save_to_csv(supplier_df, 'supplier')
    
    customer_df = generate_customer_dimension()
    save_to_csv(customer_df, 'customer')
    
    # Generate and save fact table
    print("\nGenerating fact table...")
    lineorder_df = generate_lineorder_fact(10000)  # Smaller sample for testing
    save_to_csv(lineorder_df, 'lineorder')
    
    print("\nData generation complete!")

if __name__ == "__main__":
    main()
