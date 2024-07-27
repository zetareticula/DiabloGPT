import argparse
import os
import pickle
import random
import sys
import utils
from AML.Synthetic.naru import models
from DiabloGPT.OUCausetFlowProcess.CostTraining import config

sys.path.append('../')

parser = argparse.ArgumentParser()
parser.add_argument('--phase', type=str, default='train', help='train or test')
parser.add_argument('--params', type=str, default='', help='Load existing parameters')
parser.add_argument('--workload', type=str, default='read', help='Workload type [`read`, `write`, `readwrite`]')

opt = parser.parse_args()
print(opt)

tconfig = config.TrainingConfig()
tconfig.batch_size = 64
tconfig.epoches = 20
tconfig.workload = opt.workload

if opt.phase == 'train':
    if opt.params == '':
        model = models.NARU(tconfig)
    else:
        model = models.NARU(tconfig, opt.params)
    model.train()

elif opt.phase == 'test':
    assert len(opt.params) != 0, "PARAMS should be specified when testing DDPG einstAIActor"
    model = models.NARU(tconfig, opt.params)
    model.test()

else:
    raise Exception('Wrong phase')
