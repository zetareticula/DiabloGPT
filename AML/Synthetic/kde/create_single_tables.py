# TODO:
# Path: AML/Synthetic/kde/create_single_tables.py
# Compare this snippet from DiabloGPT/OUCausetFlowProcess/LatencyTuning.py:
# # Path: DiabloGPT/OUCausetFlowProcess/LatencyTuning.py


import numpy as np
import pandas as pd
import os
import random
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable







class DDPGModel:
    def DDPG(n_states, n_actions, opt, supervised):
        assert isinstance(n_states, object)
        assert isinstance(opt, object)
        assert isinstance(supervised, object)
        model = DDPGModel(  opt, supervised)
        return model

    def DDPGModel(n_states, n_actions, opt, supervised):
        assert isinstance(n_states, object)
        model = DDPGModel(n_states, n_actions, opt, supervised)

        return model


    def __init__(self, opt, supervised):
        self.opt = opt
        self.supervised = supervised
        self.model = nn.Sequential(
            nn.Linear(self.opt.state_dim, 400),
            nn.ReLU(),
            nn.Linear(400, 300),
            nn.ReLU(),
            nn.Linear(300, self.opt.action_dim),
            nn.Tanh()
        )
        self.target_model = nn.Sequential(
            nn.Linear(self.opt.state_dim, 400),
            nn.ReLU(),
            nn.Linear(400, 300),
            nn.ReLU(),
            nn.Linear(300, self.opt.action_dim),
            nn.Tanh()
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
        self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

                self.model = nn.Sequential(
                    nn.Linear(self.opt.state_dim, 400),
                    nn.ReLU(),
                    nn.Linear(400, 300),
                    nn.ReLU(),
                    nn.Linear(300, self.opt.action_dim),
                    nn.Tanh()
                )
                self.target_model = nn.Sequential(
                    nn.Linear(self.opt.state_dim, 400),
                    nn.ReLU(),
                    nn.Linear(400, 300),
                    nn.ReLU(),
                    nn.Linear(300, self.opt.action_dim),
                    nn.Tanh()
                )
                self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

                        self.model = nn.Sequential(
                            nn.Linear(self.opt.state_dim, 400),
                            nn.ReLU(),
                            nn.Linear(400, 300),
                            nn.ReLU(),
                            nn.Linear(300, self.opt.action_dim),
                            nn.Tanh()
                        )
                        self.target_model = nn.Sequential(
                            nn.Linear(self.opt.state_dim, 400),
                            nn.ReLU(),
                            nn.Linear(400, 300),
                            nn.ReLU(),
                            nn.Linear(300, self.opt.action_dim),
                            nn.Tanh()
                        )
                        self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                        self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

                                        self.model = nn.Sequential(
                                            nn.Linear(self.opt.state_dim, 400),
                                            nn.ReLU(),
                                            nn.Linear(400, 300),
                                            nn.ReLU(),
                                            nn.Linear(300, self.opt.action_dim),
                                            nn.Tanh()
                                        )
                                        self.target_model = nn.Sequential(
                                            nn.Linear(self.opt.state_dim, 400),
                                            nn.ReLU(),
                                            nn.Linear(400, 300),
                                            nn.ReLU(),
                                            nn.Linear(300, self.opt.action_dim),
                                            nn.Tanh()
                                        )
                                        self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                                        self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

                                                    self.model = nn.Sequential(
                                                        nn.Linear(self.opt.state_dim, 400),
                                                        nn.ReLU(),
                                                        nn.Linear(400, 300),
                                                        nn.ReLU(),
                                                        nn.Linear(300, self.opt.action_dim),
                                                        nn.Tanh()
                                                    )
                                                    self.target_model = nn.Sequential(
                                                        nn.Linear(self.opt.state_dim, 400),
                                                        nn.ReLU(),
                                                        nn.Linear(400, 300),
                                                        nn.ReLU(),
                                                        nn.Linear(300, self.opt.action_dim),
                                                        nn.Tanh()
                                                    )
                                                    self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                                                    self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()


        else:

                                                                            self.model = nn.Sequential(
                                                                                nn.Linear(self.opt.state_dim, 400),
                                                                                nn.ReLU(),
                                                                                nn.Linear(400, 300),
                                                                                nn.ReLU(),
                                                                                nn.Linear(300, self.opt.action_dim),
                                                                                nn.Tanh()
                                                                            )
                                                                            self.target_model = nn.Sequential(
                                                                                nn.Linear(self.opt.state_dim, 400),
                                                                                nn.ReLU(),
                                                                                nn.Linear(400, 300),
                                                                                nn.ReLU(),
                                                                                nn.Linear(300, self.opt.action_dim),
                                                                                nn.Tanh()
                                                                            )
                                                                            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                                                                            self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        if self.supervised:
            self.model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.target_model = nn.Sequential(
                nn.Linear(self.opt.state_dim, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, self.opt.action_dim),
                nn.Tanh()
            )
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
            self.loss = nn.MSELoss()

        else:

                self.model = nn.Sequential(
                    nn.Linear(self.opt.state_dim, 400),
                    nn.ReLU(),
                    nn.Linear(400, 300),
                    nn.ReLU(),
                    nn.Linear(300, self.opt.action_dim),
                    nn.Tanh()
                )
                self.target_model = nn.Sequential(
                    nn.Linear(self.opt.state_dim, 400),
                    nn.ReLU(),
                    nn.Linear(400, 300),
                    nn.ReLU(),
                    nn.Linear(300, self.opt.action_dim),
                    nn.Tanh()
                )
                self.optimizer = optim.Adam(self.model.parameters(), lr=self.opt.lr)
                self.loss = nn.MSELoss()

def create_single_script_generate(file_path, database, table_name):
    sqls = []
    sqls.append(
        'CREATE TABLE IF NOT EXISTS {} ({});'.format(table_name, ','.join([x + ' FLOAT' for x in ['col0', 'col1']])))
    sqls.append("\copy {} FROM '{}' CSV HEADER;".format(table_name, '{}'.format(file_path)))
    with open('script.sql', 'w') as f:
        # we need to create the table first
        for sql in sqls:
            f.write(sql)
            f.write('\n')


if __name__ == '__main__':



    import argparse
    from itertools import combinations
    from os import listdir
    from os.path import isfile, join


#     def create_joins_script(join_sample_dir, database, join_sample=None, f=None, _dir=None):
#         join_files = [f for f in listdir(join_sample_dir) if isfile(join_sample
# _dir + '/' + f) and f.endswith('.csv')]  # only files that end with .csv
#
#
#
#
#
#         if join_sample:
#             join_files = [join_sample]
#
#
#         for join_file in join_files:
#             table_name = join_file.split('.')[0]
#             create_single_script_generate(join_sample_dir + '/' + join_file, database, table_name)


    parser = argparse.ArgumentParser(description='Create Join Samples.')
    parser.add_argument('--path', type=str)
    parser.add_argument('--database', type=str)
    parser.add_argument('--table-name', type=str)
    args = parser.parse_args()
    create_single_script_generate(args.path, args.database, args.table_name)


# Path: DiabloGPT/OUCausetFlowProcess/LatencyTuning.py
