#!/usr/bin/env python3
"""
Test script to run MUMFORDGRAMMAR with a small test dataset.
"""
import os
import sys
from MUMFORDGRAMMAR.train import main as train_main
from MUMFORDGRAMMAR.data import get_train_datasets, load_data, make_dataset
from MUMFORDGRAMMAR.model import SetConv
from MUMFORDGRAMMAR.util import *

def run_test():
    """Run a test of the MUMFORDGRAMMAR training with a small dataset."""
    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'MUMFORDGRAMMAR', 'data')
    test_data_dir = os.path.join(base_dir, 'test_data')
    
    # Use a small min-max file from the data directory
    min_max_file = os.path.join(data_dir, 'cols_2_distinct_1000_corr_2_skew_2_min_max_vals.csv')
    
    # Create a simple train and test SQL file
    train_sql_file = os.path.join(test_data_dir, 'train_queries.sql')
    test_sql_file = os.path.join(test_data_dir, 'test_queries.sql')
    
    print(f"Using min-max file: {min_max_file}")
    print(f"Using train SQL file: {train_sql_file}")
    print(f"Using test SQL file: {test_sql_file}")
    
    # Run training with a small number of epochs for testing
    train_args = [
        '--min-max-file', min_max_file,
        '--queries', '100',  # Small number of queries for testing
        '--epochs', '2',     # Small number of epochs for testing
        '--batch', '32',     # Small batch size for testing
        '--hid', '64',       # Smaller hidden layer size for testing
        '--train',           # Enable training
        '--train-query-file', train_sql_file,
        '--test-query-file', test_sql_file,
        '--version', 'test_run'
    ]
    
    # Add the current directory to the Python path
    sys.path.insert(0, base_dir)
    
    # Run the training
    print("Starting training...")
    train_main()

if __name__ == "__main__":
    run_test()
