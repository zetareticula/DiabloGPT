# -*- coding: utf-8 -*-

"""
Ornstein–Uhlenbeck process
"""

import numpy as np
from numpy.random import randn
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from torch.nn.utils.rnn import PackedSequence
import numpy as np
import random
import math
import time
import os
from collections import defaultdict



# Define model architecture






class OUProcess(object):
    def __init__(self, action_dim, mu=0, theta=0.15, sigma=0.2):
        self.action_dim = action_dim
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.reset()

    def reset(self):
        self.state = np.ones(self.action_dim) * self.mu

    def evolve_state(self):
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * randn(len(x))
        self.state = x + dx
        return self.state

    def __call__(self):
        return self.evolve_state()


# from https://github.com/songrotek/DDPG/blob/master/ou_noise.py
# -*- coding: utf-8 -*-