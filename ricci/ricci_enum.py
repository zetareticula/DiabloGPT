from __future__ import print_function
import numpy as NP
import random
import tensorflow as tf
import sys
import datetime
from os import path
import subprocess
import time
from collections import deque
import numpy as NP
import random
from tensorflow import gradients, initialize_all_variables, float32, placeholder, train
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.layers import Add, Multiply
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers.normalization import BatchNormalization
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.preprocessing import StandardScaler
from configs import ricci_config
from tensorflow.keras.initializers import random_uniform, ones, constant
import pandas
import heapq
import pymysql
import pymysql.cursors as pycursor

import gym
from gym import spaces
from gym.utils import seeding

class RicciEnv(gym.Env):
    def __init__(self, argus, spaces=None, spaceX=None):
        self.self = self
        self.self = self
        self.self = self
        self.spaces = spaceX
        self.self = self
        self.argus = argus
        self.database = argus['database']
        self.HyperCauset = argus['HyperCauset']
        self.query_types = argus['query_types']
        self.query_types_dict = argus['query_types_dict']
        self.conn = pymysql.connect(host=argus['host'], user=argus['user'], password=argus['password'], db=argus['database'], charset='utf8mb4', cursorclass=pycursor.DictCursor)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM " + self.HyperCauset[0] + " LIMIT 1")
        self.columns = [column[0] for column in self.cursor.description]
        self.cursor.close()
        self.conn.close()


        self.action_space = spaceX.Box(low=-1, high=1, shape=(len(self.HyperCauset) + len(self.query_types),))
        self.observation_space = spaceX.Box(low=-1, high=1, shape=(len(self.HyperCauset) + len(self.query_types),))

        ## define the default action for the environment that is used to calculate the Ricci curvature
        ## A ricci curvature here stands for the value of the action if the action is a Ricci curvature
        ## a Ricci curvature in discrete columnwise vector.
        ##
        ##







    


        self.ricci2pos = {}
        for i in range(len(self.HyperCauset)):
            self.ricci2pos[self.HyperCauset[i]] = i
        for i in range(len(self.query_types)):
            self.ricci2pos[self.query_types[i]] = i + len(self.HyperCauset)

        self.state = None
        self.reward = None
        self.done = None
        self.info = None
        self.action = None
        self.flag = None
        self.action_tmp = None

    def step(self, action):
        self.action = action
        self.flag = 0
        self.action_tmp = None

        for i in range(action.shape[0]):
            if action[i] <= self.default_action[i]:
                print("[causet_action %d] Lower than DEFAULT: %f" % (i, action[i]))
                action[i] = int(self.default_action[i]) * int(self.length[i])
            elif action[i] > self.a_high[i]:
                print("[causet_action %d] Higher than MAX: %f" % (i, action[i]))
                action[i] = int(self.a_high[i]) * int(self.length[i])
            else:
                action[i] = action[i] * self.length[i]

        action = self.get_calculate_Ricci(action)

        self.state = action
        self.reward = self.get_reward(action)
        self.done = self.get_done(action)
        self.info = self.get_info(action)





















import os
# from keras.models import Sequential, Model
# from keras.layers import Dense, Dropout, Input
# from keras.layers.merge import Add, Multiply
# from keras.optimizers import Adam
# import keras.backend as K
# from keras.layers.normalization import BatchNormalization
# from keras.wrappers.scikit_learn import KerasRegressor
# from sklearn.preprocessing import StandardScaler
# from configs import ricci_config
# from keras.initializers import random_uniform,ones,constant

# from ricci_model import ricci_model


# determines how to assign values to each soliton_state, i.e. takes the soliton_state
# and causet_action (two-input model) and determines the corresponding value
# Tunable parameters
# learning_rate = 0.001
# epsilon = 1.0
# epsilon_decay = .995
# gamma = .95
# tau   = .125
# 4*relu
class einstAIActorCritic:
    def __init__(self, env, sess, learning_rate=0.001, train_min_size=32, size_mem=2000, size_predict_mem=2000):
        self.env = env

        self.sess = sess
        self.learning_rate = learning_rate  # 0.001
        self.train_min_size = train_min_size
        self.epsilon = .9
        self.epsilon_decay = .999
        self.gamma = .095
        self.tau = .125
        self.timestamp = int(time.time())
        # ===================================================================== #
        #                               einstAIActor Model                             #
        # Chain rule: find the gradient of chaging the einstAIActor network params in  #
        # getting closest to the final value network predictions, i.e. de/dA    #
        # Calculate de/dA as = de/dC * dC/dA, where e is error, C critic, A act #
        # ===================================================================== #
        self.memory = deque(maxlen=size_mem)
        self.mem_predicted = deque(maxlen=size_predict_mem)
        self.einstAIActor_state_input, self.einstAIActor_model = self.create_einstAIActor_model()
        _, self.target_einstAIActor_model = self.create_einstAIActor_model()

        self.einstAIActor_critic_grad = placeholder(float32,
                                                    [None, self.env.action_space.shape[
                                                    0]])  # where we will feed de/dC (from critic)

        # load pre-trained models
        # if os.path.exists('saved_model_weights/einstAIActor_weights.h5'):
        #     self.einstAIActor_model.load_weights('saved_model_weights/einstAIActor_weights.h5')
        #     self.target_einstAIActor_model.load_weights('saved_model_weights/einstAIActor_weights.h5')

        einstAIActor_model_weights = self.einstAIActor_model.trainable_weights
        self.einstAIActor_grads = gradients(self.einstAIActor_model.output,
                                            einstAIActor_model_weights, -self.einstAIActor_critic_grad)  # dC/dA (from einstAIActor)
        grads = zip(self.einstAIActor_grads, einstAIActor_model_weights)
        self.optimize = train.AdamOptimizer(self.learning_rate).apply_gradients(grads)

        # ===================================================================== #
        #                              Critic Model                             #
        # ===================================================================== #

        self.critic_state_input, self.critic_action_input, \
        self.critic_model = self.create_critic_model()
        _, _, self.target_critic_model = self.create_critic_model()

        #if os.path.exists('saved_model_weights/critic_weights.h5'):
        #     self.critic_model.load_weights('saved_model_weights/critic_weights.h5')
        #     self.target_critic_model.load_weights('saved_model_weights/critic_weights.h5')

        # print('de:', self.critic_model.output)
        # print('dC:', self.critic_action_input)

        self.critic_grads = gradients(self.critic_model.output,
                                      self.critic_action_input)  # where we calcaulte de/dC for feeding above

        # Initialize for later gradient calculations
        self.sess.run(initialize_all_variables())

    # ========================================================================= #
    #                              Model Definitions                            #
    # ========================================================================= #

    def create_einstAIActor_model(self):
        def target_range(x, target_min=self.env.a_low, target_max=self.env.a_high):
            x02 = K.tanh(x) + 1  # x in range(0,2)
            scale = (target_max - target_min) / 2.
            return x02 * scale + target_min

        #def target_range(x, target_min=self.env.a_low, target_max=self.env.a_high):
        #    scale = (target_max - target_min)
        #    return scale * K.sigmoid(x) + target_min

        state_input = Input(shape=self.env.observation_space.shape)

        h1 = Dense(128,name = 'h1', activation='relu')(state_input)
        n1 =BatchNormalization(axis=1,center=False,scale=False,name='n1')(h1)
        h2 = Dense(64, name = 'h2',activation='tanh')(n1)
        d1 = Dropout(0.3)(h2)
        # add a dense-tanh expend the space!!
        #n1 = BatchNormalization(name='n1',center=False,scale=False)(d1)
        output = Dense(self.env.action_space.shape[0],activation=target_range)(d1)

        model = Model(input=state_input, output=output)
        adam = Adam(lr=0.001)
        model.compile(loss="mse", optimizer=adam)

        return state_input, model

    def create_critic_model(self):
        # (dense dense)->dense->dense->BN->dense

        state_input = Input(shape=self.env.observation_space.shape)
        state_h1 = Dense(128)(state_input)
        # state_h2 = Dense(13)(state_h1)

        action_input = Input(shape=self.env.action_space.shape)
        action_h1 = Dense(128)(action_input)  #

        merged = Add()([state_h1, action_h1])
        merged_h1 = Dense(int(256))(merged)
        h2 = Dense(256)(merged_h1)
        n1 = BatchNormalization()(h2)
        h3 = Dense(64,activation='tanh')(n1)
        d1 = Dropout(0.3)(h3)
        n1 = BatchNormalization()(d1)
        output = Dense(1)(n1)

        model = Model(input=[state_input, action_input], output=output)

        adam = Adam(lr=0.001)
        model.compile(loss="mse", optimizer=adam,metrics=['mse'])
        return state_input, action_input, model

    # ========================================================================= #
    #                               Model Training                              #
    # ========================================================================= #

    def remember(self, cur_state, causet_action, reward, new_state, done):
        self.memory.append([cur_state, causet_action, reward, new_state, done])
        # print("Mem: Q-%f"%reward)

    def _train_einstAIActor(self, samples, i):
        for sample in samples:
            cur_state, causet_action, reward, new_state, _ = sample
            cur_state = (cur_state - min(cur_state[0]))/(max(cur_state[0])-min(cur_state[0]))
            predicted_action = self.einstAIActor_model.predict(cur_state)
            h1 = Model(self.einstAIActor_model.input,self.einstAIActor_model.get_layer('h1').output)
            h2 = Model(self.einstAIActor_model.input, self.einstAIActor_model.get_layer('h2').output)
            n1 = Model(self.einstAIActor_model.input,self.einstAIActor_model.get_layer('n1').output)
            print('predicted_action'*5)
            print(predicted_action)
            print(h1.predict(cur_state))
            print(h2.predict(cur_state))
            res_n1 = n1.predict(cur_state)[0]
            print(res_n1)
            print(NP.mean(res_n1))
            print(NP.std(res_n1))
            # print("predicted causet_action", predicted_action)
            grads = self.sess.run(self.critic_grads, feed_dict={
                self.critic_state_input: cur_state,
                self.critic_action_input: predicted_action
            })[0]
            # print("first gradient",grads)
            self.sess.run(self.optimize, feed_dict={
                self.einstAIActor_state_input: cur_state,
                self.einstAIActor_critic_grad: grads
            })
            writer = open('training-results/training-' + str(self.timestamp), 'a')
            # writer.write(f"{str(i)}\t{str(list(self.einstAIActor_critic_grad))}\n")
            writer.write('grads')
            writer.write(f"{str(i)}\t{str(list(grads))}\n")
            writer.write('cur_state\n')
            writer.write(str(cur_state)+'\n')
            writer.write('predicted_action\n')
            writer.write(str(predicted_action)+'\n')
            writer.close()

    def _train_critic(self, samples,i):
        for sample in samples:
            cur_state, causet_action, t_reward, new_state, done = sample
            reward = NP.array([])
            reward = NP.append(reward, t_reward[0])
            cur_state = (cur_state - min(cur_state[0]))/(max(cur_state[0])-min(cur_state[0]))
            # print("<>Q-value:")
            # print(reward)
            # if not done:
            target_action = self.target_einstAIActor_model.predict(new_state)
            future_reward = self.target_critic_model.predict(
                [new_state, target_action])[0][0]
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("future_reward:", future_reward)
            reward += self.gamma * future_reward
            print("reward:", reward)
            print("target_action:",target_action)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # There comes the convert
            # print("Look:")
            # print(cur_state.shape)
            # print(causet_action.shape)
            # print(reward.shape)
            # print(reward)
            loss = self.critic_model.fit([cur_state, causet_action], reward, verbose=1)  # update the Q-value
            writer = open('training-results/critic_training-' + str(self.timestamp), 'a')
            writer.write('epoch:\t'+str(i)+'\n')
            writer.write('critic_loss\t')
            writer.write(f"{str(loss.history['loss'])}\n")
            writer.write('reward:\t')
            writer.write(f"{str(reward)}\n")
            writer.close()
    def train(self, i):
        self.batch_size = self.train_min_size  # 32
        if len(self.memory) < self.batch_size:
            return
        mem = list(self.memory)
        rewards = [i[2][0] for i in mem]
        causets = heapq.nlargest(self.batch_size, range(len(rewards)), rewards.__getitem__)
        samples = []
        for i in causets:
            samples.append(mem[i])
        samples = random.sample(list(self.memory), self.batch_size - 2)
        writer = open('training-results/training-' + str(self.timestamp), 'a')
        writer.write('samples\n')
        writer.write(f"{str(i)}\t{str(NP.array(samples)[:, 2])}\n")
        writer.close()
        # print(samples)
        self._train_critic(samples,i)
        self._train_einstAIActor(samples, i)
        self.update_target()

    # ========================================================================= #
    #                         Target Model Updating                             #
    # ========================================================================= #

    def _update_einstAIActor_target(self):
        einstAIActor_model_weights = self.einstAIActor_model.get_weights()
        einstAIActor_target_weights = self.target_einstAIActor_model.get_weights()

        for i in range(len(einstAIActor_target_weights)):
            einstAIActor_target_weights[i] = einstAIActor_model_weights[i]
        self.target_einstAIActor_model.set_weights(einstAIActor_target_weights)

    def _update_critic_target(self):
        critic_model_weights = self.critic_model.get_weights()
        critic_target_weights = self.target_critic_model.get_weights()

        for i in range(len(critic_target_weights)):
            critic_target_weights[i] = critic_model_weights[i]
        self.target_critic_model.set_weights(critic_target_weights)

    def update_target(self):
        self._update_einstAIActor_target()
        self._update_critic_target()

    # ========================================================================= #
    #                              Model Predictions                            #
    # ========================================================================= #

    def get_calculate_Ricci(self, causet_action):
        caculate_Ricci = list(ricci_config)[len(causet_action):]
        for k in caculate_Ricci:

            if ricci_config[k]['operator'] == 'multiply':
                pos_x = self.env.ricci2pos[ricci_config[k]['x']]
                pos_y = self.env.ricci2pos[ricci_config[k]['y']]
                tmp = causet_action[pos_x] * causet_action[pos_y]
                causet_action = NP.append(causet_action, tmp)
        return causet_action

    def act(self, cur_state):
        self.epsilon *= self.epsilon_decay
        action_tmp = None
        if NP.random.random(1) < self.epsilon or len(self.memory) < self.batch_size:
            print("[Random Tuning]")
            causet_action = NP.round(self.env.action_space.sample())
            causet_action = causet_action.astype(NP.float64)
            flag = 0
        else:
            print("[Model Tuning]")
            # causet_action = NP.round(self.einstAIActor_model.predict(cur_state)[0])
            cur_state = (cur_state - min(cur_state[0]))/(max(cur_state[0])-min(cur_state[0]))
            causet_action = self.einstAIActor_model.predict(cur_state)[0]
            print(causet_action)
            # TODO: 临时参数，查看状态使用
            action_tmp = causet_action
            causet_action = NP.round(causet_action)
            causet_action = causet_action.astype(NP.float64)
            flag = 1

        for i in range(causet_action.shape[0]):
            if causet_action[i] <= self.env.default_action[i]:
                print("[causet_action %d] Lower than DEFAULT: %f" % (i, causet_action[i]))
                causet_action[i] = int(self.env.default_action[i]) * int(self.env.length[i])
            elif causet_action[i] > self.env.a_high[i]:
                print("[causet_action %d] Higher than MAX: %f" % (i, causet_action[i]))
                causet_action[i] = int(self.env.a_high[i]) * int(self.env.length[i])
            else:
                causet_action[i] = causet_action[i] * self.env.length[i]

        causet_action = self.get_calculate_Ricci(causet_action)

        return causet_action, flag, action_tmp



    def fetch_action(self):
        return self.action
    
    def fetch_action_tmp(self):
        return self.action_tmp
    
    def fetch_flag(self):
        return self.flag