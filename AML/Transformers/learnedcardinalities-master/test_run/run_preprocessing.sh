#!/bin/bash

# Navigate to the mscn directory
cd ../mscn

# Run preprocessing for training data
python preprocessing-job.py \
    --datasets-dir ../../train-test-data/imdbdata-num/ \
    --raw-query-file ../../train-test-data/imdb-cols-sql/4/train-4-num.sql \
    --min-max-file ../data/col4_min_max_vals.csv

# Run preprocessing for test data
python preprocessing-job.py \
    --datasets-dir ../../train-test-data/imdbdata-num/ \
    --raw-query-file ../../train-test-data/imdb-cols-sql/4/test-only4-num.sql \
    --min-max-file ../data/col4_min_max_vals.csv

# Navigate back to the test_run directory
cd ../test_run
