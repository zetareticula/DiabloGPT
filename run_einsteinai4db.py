#!/usr/bin/env python3
"""
Test script to run EINSTEINAI4DB with the SSB (Star Schema Benchmark) dataset.
"""
import os
import sys
import logging
from pathlib import Path

# Add the necessary directories to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'AML', 'Synthetic', 'EINSTEINAI4DB'))
sys.path.append(os.path.join(project_root, 'AML', 'Synthetic', 'EINSTEINAI4DB', 'ensemble_creation'))
sys.path.append(os.path.join(project_root, 'AML', 'Synthetic', 'EINSTEINAI4DB', 'epigraph'))
sys.path.append(os.path.join(project_root, 'AML', 'Synthetic', 'EINSTEINAI4DB', 'deep_rl'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the EINSTEINAI4DB module with the SSB dataset."""
    try:
        logger.info("Starting EINSTEINAI4DB test with SSB dataset...")
        
        # Import required modules
        from schemas.ssb.schema import gen_mini_ssb_schema
        from ensemble_creation.naive import create_naive_all_split_ensemble
        from ensemble_creation.aqp_evaluation import evaluate_aqp_queries
        
        # Set up paths
        data_dir = os.path.join(project_root, 'data', 'ssb')
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate the SSB schema
        logger.info("Generating SSB schema...")
        schema = gen_mini_ssb_schema(data_dir)
        
        # Set up ensemble parameters
        hdf_path = os.path.join(data_dir, 'ssb_data.hdf')
        ensemble_path = os.path.join(data_dir, 'ensemble')
        sample_size = 1000  # Number of samples to use for training
        
        # Create the ensemble
        logger.info("Creating naive ensemble...")
        create_naive_all_split_ensemble(
            schema=schema,
            hdf_path=hdf_path,
            sample_size=sample_size,
            ensemble_path=ensemble_path,
            dataset='ssb',
            bloom_filters=None,
            rdc_threshold=0.3,
            max_table_data=10000,
            post_sampling_factor=10,
            incremental_learning_rate=0.1
        )
        
        logger.info("Ensemble created successfully!")
        
        # Example of how to evaluate AQP queries (you'll need to provide actual queries)
        # evaluate_aqp_queries(
        #     ensemble_location=ensemble_path,
        #     query_filename=os.path.join(data_dir, 'queries.sql'),
        #     target_path=os.path.join(data_dir, 'results'),
        #     schema=schema,
        #     ground_truth_path=os.path.join(data_dir, 'ground_truth.pkl'),
        #     rdc_spn_selection=False
        # )
        
    except Exception as e:
        logger.error(f"Error running EINSTEINAI4DB: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
