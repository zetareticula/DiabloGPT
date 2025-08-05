#!/bin/bash

# Navigate to the parent directory
cd ..

# Run training with a small number of epochs for testing
python train.py \
    --queries 1000 \
    --epochs 5 \
    --batch 128 \
    --hid 128 \
    --train-query-file train-test-data/imdb-cols-sql/4/train-4-num.sql \
    --test-query-file train-test-data/imdb-cols-sql/4/test-only4-num.sql \
    --min-max-file data/col4_min_max_vals.csv \
    --train

# Run evaluation
python train.py \
    --queries 1000 \
    --epochs 5 \
    --batch 128 \
    --hid 128 \
    --train-query-file train-test-data/imdb-cols-sql/4/train-4-num.sql \
    --test-query-file train-test-data/imdb-cols-sql/4/test-only4-num.sql \
    --min-max-file data/col4_min_max_vals.csv
