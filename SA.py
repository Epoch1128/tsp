import math
import os
import numpy as np
import random
from math import e, inf
from numpy.core.fromnumeric import sort
from utils import get_map, map_to_graph
from config import *
from tqdm import tqdm

def cal_cost(graph, traj_list):
    cost = 0
    for i in range(len(traj_list) - 1):
        cost = cost + graph[traj_list[i]][traj_list[i+1]]
    return cost + graph[traj_list[-1]][traj_list[0]]

def generate_random_seeds(max_num):
    x = random.sample(range(max_num + 1), 2)
    return min(x[0], x[1]), max(x[0], x[1])

def is_equal(a, b, error):
    if abs(a - b) < error:
        return True
    else:
        return False

def SA(num_city, map, origin_temp, iter_times, temp_decay):
    """
    Simulated annealing algorithm
    Parameters:
    graph: distance map
    map: coordinates map
    origin_traj_list: original number list [1, 2, 3, ..., num_city]
    origin_temp: temperature at time 0
    iter_times: max times of iteration
    temp_decay: the decay of temperature
    Return:
    None
    """
    graph = map_to_graph(map, num_city)
    last_cost = inf
    last_list = [i for i in range(num_city)]
    now_cost = cal_cost(graph, traj_list=last_list)
    t = origin_temp
    step = 0
    while not is_equal(now_cost, last_cost, 1e-3):
        last_cost = now_cost
        last_iter_cost = now_cost
        for _ in range(iter_times):
            step = step + 1
            u, v = generate_random_seeds(num_city)
            new_list_1 = last_list[:u]
            new_list_2 = list(reversed(last_list[u:v]))
            new_list_3 = last_list[v:]
            new_list = new_list_1 + new_list_2 + new_list_3
            now_iter_cost = last_iter_cost + graph[
                new_list[u-1]][new_list[u]] + graph[new_list[v-1]][new_list[v % num_city]] - graph[
                    last_list[u-1]][last_list[u]] - graph[last_list[v-1]][last_list[v % num_city]]
            # now_iter_cost = cal_cost(graph, new_list)
            if now_iter_cost <  last_iter_cost:
                last_list = new_list
                last_iter_cost = now_iter_cost
            elif now_iter_cost > last_iter_cost:
                pro = math.exp(-(now_iter_cost-last_iter_cost)/t)
                random_bond = np.random.rand()
                if pro > random_bond:
                    # state convert
                    last_list = new_list
                    last_iter_cost = now_iter_cost

        # balance at temperature t
        now_cost = last_iter_cost
        t = t * temp_decay

    return round(now_cost, 2), last_list

if __name__ == '__main__':
    result_list = []
    result = []
    time = []
    for _ in tqdm(range(iters)):
        loss, traj = SA(num_city=num_city, map=map,
                        origin_temp=t0, iter_times=l, temp_decay=alpha)
        result_list.append([loss, traj])
    for item in result_list:
        if item not in result:
            result.append(item)
            time.append(1)
        else:
            id = result.index(item)
            time[id] = time[id] + 1
    for i in range(len(time)):
        result[i].append(time[i])
    result = sorted(result, key=lambda x: x[0])
    if SA_mode == "demo":
        for i, item in enumerate(result):
            get_map(np.array([map[index] for index in item[1]]), rank=i)
            print("The top_{} distance is {}. The trajactory is {}. The repeat time is {}".format(i + 1, item[0], item[1], item[2]))
    elif SA_mode == "exp":
        exp_result = []
        exp_times = []
        for i, item in enumerate(result):
            if item[0] not in exp_result:
                exp_result.append(item[0])
                exp_times.append(item[2])
            else:
                idx = exp_result.index(item[0])
                exp_times[idx] = exp_times[idx] + 1
        for i in range(len(exp_result)):
            print("Loss: {}; Ratio:{}".format(exp_result[i], round(exp_times[i] / iters, 4)))

