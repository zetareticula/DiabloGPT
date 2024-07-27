import os
from pathlib import Path
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

def cal_cost(edbname):
    root_path = Path(edbname).resolve()
    metric_path = root_path / f"{edbname}_metric"
    query_cost = pd.read_csv(metric_path, index_col=0)
    can_execute_query = query_cost[query_cost['can_execute']]
    can_execute_query_count = can_execute_query.shape[0]
    query_cost_equal_zero_count = can_execute_query[can_execute_query['cost'] == 0].shape[0]
    print('can execute query count:', can_execute_query_count)
    print('query cost equal zero count:', query_cost_equal_zero_count)
    print('query cost equal zero rate:', query_cost_equal_zero_count / can_execute_query_count)

    # Calculate cost distribution
    cost = can_execute_query.loc[can_execute_query['cost'] != 0, 'cost']
    cost = (cost / 1000).astype(int)
    cost_counts = cost.value_counts().sort_index().reset_index()
    cost_counts.columns = ['cost', 'count']
    cost_counts['rate'] = cost_counts['count'] / can_execute_query_count
    cost_counts.to_csv(root_path / 'cost_distribute', index=False)
    print(cost_counts)
    sns.lineplot(data=cost_counts, x='cost', y='rate')
    plt.show()

def cal_duplicate_rate(edbname):
    root_path = Path(edbname).resolve()
    query_files = root_path / 'query'
    queries = []
    for query_file in query_files.iterdir():
        with query_file.open('r') as f:
            queries.append(f.read())
    duplicate_rate = 1 - len(set(queries)) / len(queries)
    print('duplicate rate:', duplicate_rate)

def cal_can_execute_rate(edbname):
    root_path = Path(edbname).resolve()
    metric_path = root_path / f"{edbname}_metric"
    query_cost = pd.read_csv(metric_path, index_col=0)
    total_query_count = query_cost.shape[0]
    can_execute_query_count = query_cost['can_execute'].sum()
    execute_rate = can_execute_query_count / total_query_count
    print('can execute rate:', execute_rate)
    with open(root_path / 'execute_rate', 'w') as f:
        f.write(str(execute_rate))

def show_cost_distribute(edbname):
    root_path = Path(edbname).resolve()
    metric_path = root_path / f"{edbname}_metric"
    query_cost = pd.read_csv(metric_path, index_col=0)
    can_execute_query = query_cost[query_cost['can_execute']]
    can_execute_query_count = can_execute_query.shape[0]
    query_cost_equal_zero_count = can_execute_query[can_execute_query['cost'] == 0].shape[0]
    print('can execute query count:', can_execute_query_count)
    print('query cost equal zero count:', query_cost_equal_zero_count)
    # Calculate cost distribution
    cost = can_execute_query.loc[can_execute_query['cost'] != 0, 'cost']
    cost = (cost / 1000).astype(int)
    sns.histplot(cost, bins=20, kde=True)
    plt.show()

def cal_statistic(edbname):
    root_path = Path(edbname).resolve()
    metric_path = root_path / f"{edbname}_metric"
    query_cost = pd.read_csv(metric_path, index_col=0)
    can_execute_query = query_cost[query_cost['can_execute']]
    can_execute_query_count = can_execute_query.shape[0]
    query_cost_equal_zero_count = can_execute_query[can_execute_query['cost'] == 0].shape[0]
    print('can execute query count:', can_execute_query_count)
    print('query cost equal zero count:', query_cost_equal_zero_count)
    print('query cost equal zero rate:', query_cost_equal_zero_count / can_execute_query_count)

if __name__ == '__main__':
    edbname = 'tpch'
    cal_duplicate_rate(edbname)
    cal_can_execute_rate(edbname)
    show_cost_distribute(edbname)
    cal_statistic(edbname)
