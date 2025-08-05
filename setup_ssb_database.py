#!/usr/bin/env python3
"""
Set up a PostgreSQL database and load the SSB data.
"""
import os
import psycopg2
from psycopg2 import sql
import pandas as pd
from pathlib import Path

# Database configuration
DB_CONFIG = {
    'dbname': 'ssb_db',
    'user': 'postgres',
    'password': 'postgres',  # Change this to your PostgreSQL password
    'host': 'localhost',
    'port': '5432'
}

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'ssb')

def create_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_database():
    """Create the SSB database if it doesn't exist."""
    # Connect to the default 'postgres' database to create a new database
    temp_config = DB_CONFIG.copy()
    temp_config['dbname'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**temp_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['dbname'],))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {DB_CONFIG['dbname']}...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_CONFIG['dbname']))
            )
            print("Database created successfully!")
        else:
            print(f"Database {DB_CONFIG['dbname']} already exists.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables():
    """Create the SSB tables in the database."""
    conn = create_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Drop tables if they exist
    drop_queries = [
        "DROP TABLE IF EXISTS lineorder CASCADE",
        "DROP TABLE IF EXISTS customer CASCADE",
        "DROP TABLE IF EXISTS supplier CASCADE",
        "DROP TABLE IF EXISTS part CASCADE",
        "DROP TABLE IF EXISTS dwdate CASCADE"
    ]
    
    for query in drop_queries:
        cursor.execute(query)
    
    # Create dimension tables
    create_queries = ["""
        CREATE TABLE dwdate (
            d_datekey INTEGER PRIMARY KEY,
            d_date DATE,
            d_dayofweek INTEGER,
            d_month INTEGER,
            d_year INTEGER,
            d_yearmonthnum INTEGER,
            d_yearmonth VARCHAR(7),
            d_weeknuminyear INTEGER,
            d_sellingseason VARCHAR(10),
            d_lastdayinweekfl INTEGER,
            d_holidayfl INTEGER,
            d_weekdayfl INTEGER
        )
    """, """
        CREATE TABLE part (
            p_partkey INTEGER PRIMARY KEY,
            p_name VARCHAR(50),
            p_mfgr VARCHAR(10),
            p_category VARCHAR(20),
            p_brand VARCHAR(20),
            p_color VARCHAR(10),
            p_type VARCHAR(20),
            p_size INTEGER,
            p_container VARCHAR(10)
        )
    """, """
        CREATE TABLE supplier (
            s_suppkey INTEGER PRIMARY KEY,
            s_name VARCHAR(50),
            s_address VARCHAR(100),
            s_city VARCHAR(50),
            s_nation VARCHAR(50),
            s_region VARCHAR(20),
            s_phone VARCHAR(20)
        )
    """, """
        CREATE TABLE customer (
            c_custkey INTEGER PRIMARY KEY,
            c_name VARCHAR(50),
            c_address VARCHAR(100),
            c_city VARCHAR(50),
            c_nation VARCHAR(50),
            c_region VARCHAR(20),
            c_phone VARCHAR(20),
            c_mktsegment VARCHAR(20)
        )
    """, """
        CREATE TABLE lineorder (
            lo_orderkey INTEGER,
            lo_linenumber INTEGER,
            lo_custkey INTEGER,
            lo_partkey INTEGER,
            lo_suppkey INTEGER,
            lo_orderdate INTEGER,
            lo_orderpriority VARCHAR(15),
            lo_shippriority VARCHAR(10),
            lo_quantity INTEGER,
            lo_extendedprice DECIMAL(15, 2),
            lo_ordtotalprice DECIMAL(15, 2),
            lo_discount DECIMAL(5, 4),
            lo_revenue DECIMAL(15, 2),
            lo_supplycost DECIMAL(15, 2),
            lo_tax DECIMAL(5, 4),
            lo_commitdate INTEGER,
            lo_shipmode VARCHAR(10),
            PRIMARY KEY (lo_orderkey, lo_linenumber),
            FOREIGN KEY (lo_custkey) REFERENCES customer(c_custkey),
            FOREIGN KEY (lo_partkey) REFERENCES part(p_partkey),
            FOREIGN KEY (lo_suppkey) REFERENCES supplier(s_suppkey),
            FOREIGN KEY (lo_orderdate) REFERENCES dwdate(d_datekey)
        )
    """]
    
    try:
        for query in create_queries:
            cursor.execute(query)
        conn.commit()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def load_data():
    """Load data from CSV files into the database."""
    conn = create_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Define table names and their corresponding CSV files
    tables = [
        ('customer', 'customer.csv'),
        ('supplier', 'supplier.csv'),
        ('part', 'part.csv'),
        ('dwdate', 'date.csv'),
        ('lineorder', 'lineorder.csv')
    ]
    
    try:
        for table, filename in tables:
            csv_path = os.path.join(DATA_DIR, filename)
            if not os.path.exists(csv_path):
                print(f"CSV file not found: {csv_path}")
                continue
                
            print(f"Loading data into {table} table...")
            with open(csv_path, 'r') as f:
                cursor.copy_expert(f"COPY {table} FROM STDIN WITH CSV HEADER", f)
            conn.commit()
            print(f"Data loaded into {table} table.")
            
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def create_indexes():
    """Create indexes to improve query performance."""
    conn = create_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    index_queries = [
        "CREATE INDEX idx_lineorder_custkey ON lineorder(lo_custkey)",
        "CREATE INDEX idx_lineorder_partkey ON lineorder(lo_partkey)",
        "CREATE INDEX idx_lineorder_suppkey ON lineorder(lo_suppkey)",
        "CREATE INDEX idx_lineorder_orderdate ON lineorder(lo_orderdate)",
        "CREATE INDEX idx_part_brand ON part(p_brand)",
        "CREATE INDEX idx_part_category ON part(p_category)",
        "CREATE INDEX idx_customer_region ON customer(c_region)",
        "CREATE INDEX idx_customer_nation ON customer(c_nation)",
        "CREATE INDEX idx_supplier_region ON supplier(s_region)",
        "CREATE INDEX idx_dwdate_year ON dwdate(d_year)",
        "CREATE INDEX idx_dwdate_month ON dwdate(d_month)"
    ]
    
    try:
        for query in index_queries:
            cursor.execute(query)
        conn.commit()
        print("Indexes created successfully!")
    except Exception as e:
        print(f"Error creating indexes: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function to set up the SSB database."""
    print("Setting up SSB database...")
    
    # Create database
    create_database()
    
    # Create tables
    create_tables()
    
    # Load data
    load_data()
    
    # Create indexes
    create_indexes()
    
    print("\nSSB database setup complete!")

if __name__ == "__main__":
    main()
