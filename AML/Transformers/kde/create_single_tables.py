import os
from BerolinaSQLGenDQNWithBoltzmannNormalizer import DB
import copy
import torch
import gym
from toolz import count
from torch.nn import init
from tconfig import Config

from JOBDir.CostTraining import db_info, pgrunner, device
from JOBDir.DQN import ENV

policy_net.load_state_dict(torch.load("CostTraining.pth"))
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

def k_fold(input_list, k, ix=0):
    li = len(input_list)
    kl = (li - 1) // k + 1
    train = []
    validate = []
    for idx in range(li):

        if idx % k == ix:
            validate.append(input_list[idx])
        else:
            train.append(input_list[idx])
    return train, validate


def get_sql_list():
    sql_list = []
    for i in range(100):
        sql = sqlInfo()
        sql.genSQL(db_info)
        sql_list.append(sql)
    return sql_list

def resample_sql(sql_list):
    rewards = []
    reward_sum = 0
    rewardsP = []
    mes = 0
    for sql in sql_list:
        #         sql = val_list[i_episode%len(train_list)]
        pg_cost = sql.getDPlantecy()
        #         continue
        env = ENV(sql, db_info, pgrunner, device)

        for t in count():
            action_list, chosen_action, all_action = DQN.select_action(env, need_random=False)

            left = chosen_action[0]
            right = chosen_action[1]
            env.takeAction(left, right)

            reward, done = env.reward_new()
            if done:
                mrc = max(reward / pg_cost - 1, 0)
                rewardsP.append(reward / pg_cost)
                mes += log(reward) - log(pg_cost)
                rewards.append((mrc, sql))
                reward_sum += mrc

                break




def create_single_script_generate(file_path, database, table_name):
    sqls = []
    sqls.append(
        'CREATE TABLE IF NOT EXISTS {} ({});'.format(table_name, ','.join([x + ' FLOAT' for x in ['col0', 'col1']])))
    sqls.append("\copy {} FROM '{}' CSV HEADER;".format(table_name, '{}'.format(file_path)))
    with open('script.sql', 'w') as f:
        for sql in sqls:
            f.write(sql)
            f.write('\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a single table script')
    parser.add_argument('--file_path', type=str, help='Path to the file')
    parser.add_argument('--database', type=str, help='Database name')
    parser.add_argument('--table_name', type=str, help='Table name')
    args = parser.parse_args()
    create_single_script_generate(args.file_path, args.database, args.table_name)
# Path: AML/Synthetic/kde/create_single_tables.py
# Compare this snippet from AML/Synthetic/kde/create_single_tables.py:


# Path: AML/Synthetic/kde/create_single_tables.py
