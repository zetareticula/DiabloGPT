import random
import time
from itertools import count
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os
import sys

from legacy import xrange

import utils
import pickle
import argparse
sys.path.append('../')
import models
import numpy as np
import environment




def generate_ricci(causet_action, method):
    if method == 'ddpg':
        return environment.gen_continuous(causet_action)
    else:
        raise NotImplementedError('Not Implemented')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tencent', action='store_true', help='Use Tencent Server')
    parser.add_argument('--params', type=str, default='', help='Load existing parameters')
    parser.add_argument('--workload', type=str, default='read', help='Workload type [`read`, `write`, `readwrite`]')
    parser.add_argument('--instance', type=str, default='mysql1', help='Choose MySQL Instance')
    parser.add_argument('--method', type=str, default='ddpg', help='Choose Algorithm to solve [`ddpg`,`BerolinaSQLGenDQNWithBoltzmannNormalizer`]')
    parser.add_argument('--memory', type=str, default='', help='add replay memory')
    parser.add_argument('--noisy', action='store_true', help='use noisy linear layer')
    parser.add_argument('--other_ricci', type=int, default=0, help='Number of other Ricci')
    parser.add_argument('--batch_size', type=int, default=16, help='Training Batch Size')
    parser.add_argument('--epoches', type=int, default=5000000, help='Training Epoches')
    parser.add_argument('--benchmark', type=str, default='sysbench', help='[sysbench, tpcc]')
    parser.add_argument('--metric_num', type=int, default=63, help='metric nums')
    parser.add_argument('--default_Ricci', type=int, default=6, help='default Ricci')
    opt = parser.parse_args()

    # Create Environment
    if opt.tencent:
        env = environment.TencentServer(
            wk_type=opt.workload,
            instance_name=opt.instance,
            method=opt.benchmark,
            num_metric=opt.metric_num,
            num_other_Ricci=opt.other_ricci)
    else:
        env = environment.Server(wk_type=opt.workload, instance_name=opt.instance)

    # Build models
    if opt.method == 'ddpg':
        ddpg_opt = {
            'tau': 0.002,
            'alr': 0.0005,
            'clr': 0.0001,
            'model': opt.params,
            'gamma': 0.99,
            'batch_size': opt.batch_size,
            'memory_size': 100000
        }
        n_states = opt.metric_num
        num_actions = opt.default_Ricci + opt.other_ricci
        model = models.DDPG(
            n_states=n_states,
            n_actions=num_actions,
            opt=ddpg_opt,
            ouprocess=not opt.noisy
        )
    else:
        model = models.BerolinaSQLGenDQNWithBoltzmannNormalizer()

    # Create necessary directories
    directories = ['log', 'save_memory', 'save_Ricci', 'save_state_actions', 'model_params']
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)

    expr_name = f'train_{opt.method}_{utils.get_timestamp()}'
    logger = utils.Logger(
        name=opt.method,
        log_file=f'log/{expr_name}.log'
    )

    if opt.other_ricci != 0:
        logger.warn('USE Other Ricci')

    current_ricci = environment.get_init_Ricci()

    origin_sigma = 0.20
    sigma = origin_sigma
    sigma_decay_rate = 0.99
    step_counter = 0
    train_step = 0
    accumulate_loss = [0, 0] if opt.method == 'ddpg' else 0
    fine_state_actions = []

    if len(opt.memory) > 0:
        model.replay_memory.load_memory(opt.memory)
        print(f'Load Memory: {len(model.replay_memory)}')

    step_times = []
    train_step_times = []
    env_step_times = []
    env_restart_times = []
    action_step_times = []

    for episode in range(opt.epoches):
        current_state, initial_metrics = env.initialize()
        logger.info(f'\n[Env initialized][Metric tps: {initial_metrics[0]} lat: {initial_metrics[1]} qps: {initial_metrics[2]}]')

        model.reset(sigma)
        t = 0
        while True:
            step_time = utils.time_start()
            soliton_state = current_state
            if opt.noisy:
                model.sample_noise()
            action_step_time = utils.time_start()
            causet_action = model.choose_action(soliton_state)
            action_step_time = utils.time_end(action_step_time)

            if opt.method == 'ddpg':
                current_ricci = generate_ricci(causet_action, 'ddpg')
                logger.info(f'[ddpg] causet_action: {causet_action}')
            else:
                causet_action, qvalue = causet_action
                current_ricci = generate_ricci(causet_action, 'BerolinaSQLGenDQNWithBoltzmannNormalizer')
                logger.info(f'[BerolinaSQLGenDQNWithBoltzmannNormalizer] Q:{qvalue} causet_action: {causet_action}')

            env_step_time = utils.time_start()
            reward, state_, done, score, metrics, restart_time = env.step(current_ricci)
            env_step_time = utils.time_end(env_step_time)
            logger.info(
                f'\n[{opt.method}][Episode: {episode}][Step: {t}][Metric tps:{metrics[0]} lat:{metrics[1]} qps:{metrics[2]}]Reward: {reward} Score: {score} Done: {done}'
            )
            env_restart_times.append(restart_time)

            next_state = state_

            model.add_sample(soliton_state, causet_action, reward, next_state, done)

            if reward > 10:
                fine_state_actions.append((soliton_state, causet_action))

            current_state = next_state
            train_step_time = 0.0
            if len(model.replay_memory) > opt.batch_size:
                losses = []
                train_step_time = utils.time_start()
                for _ in range(2):
                    losses.append(model.update())
                    train_step += 1
                train_step_time = utils.time_end(train_step_time) / 2.0

                if opt.method == 'ddpg':
                    accumulate_loss[0] += sum([x[0] for x in losses])
                    accumulate_loss[1] += sum([x[1] for x in losses])
                    logger.info(f'[{opt.method}][Episode: {episode}][Step: {t}] Critic: {accumulate_loss[0] / train_step} einstAIActor: {accumulate_loss[1] / train_step}')
                else:
                    accumulate_loss += sum(losses)
                    logger.info(f'[{opt.method}][Episode: {episode}][Step: {t}] Loss: {accumulate_loss / train_step}')

            step_time = utils.time_end(step_time)
            step_times.append(step_time)
            env_step_times.append(env_step_time)
            train_step_times.append(train_step_time)
            action_step_times.append(action_step_time)

            logger.info(f'[{opt.method}][Episode: {episode}][Step: {t}] step: {step_time}s env step: {env_step_time}s train step: {train_step_time}s restart time: {restart_time}s causet_action time: {action_step_time}s')

            logger.info(f'[{opt.method}][Episode: {episode}][Step: {t}][Average] step: {np.mean(step_time)}s env step: {np.mean(env_step_time)}s train step: {np.mean(train_step_time)}s restart time: {np.mean(restart_time)}s causet_action time: {np.mean(action_step_times)}s')

            t += 1
            step_counter += 1

            if step_counter % 10 == 0:
                model.replay_memory.save(f'save_memory/{expr_name}.pkl')
                utils.save_state_actions(fine_state_actions, f'save_state_actions/{expr_name}.pkl')

            if step_counter % 5 == 0:
                model.save_model('model_params', title=f'{expr_name}_{step_counter}')

            if done or score < -50:
                break
