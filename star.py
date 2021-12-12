from typing import List
import numpy as np
from config import *
from utils import map_to_graph


def A_star(graph, num_of_city, start_point):
    """
    start_point: [point id, cost, num_layer] e.g. [0, 0, 0]
    """
    open_list = []
    closed_list = []
    open_list.append(start_point)
    step = 0
    while len(open_list) != 0:
        step += 1
        if step > max_step:
            break
        open_list = sorted(open_list, key=lambda x: x[1])
        tgt = open_list.pop(0)
        closed_list.append(tgt)
        if len(tgt[0]) == num_of_city:
            return tgt
        # 扩展tgt
        for i in range(num_of_city):
            if i not in tgt[0]:
                x = [item for item in tgt[0]]
                x.append(i)
                tmp = [x,
                       tgt[1] + tgt[2] + 1 + graph[tgt[0][-1]][i],
                       tgt[2] + 1]
                if tmp not in open_list and tmp not in closed_list:
                    open_list.append(tmp)
    return None


if __name__ == '__main__':
    result_list = []
    for i in range(num_city):
        result_list.append(A_star(graph=map_to_graph(map, num_city), start_point=[[i], 0, 0], num_of_city=num_city))
    if len(result_list) != 0 and None not in result_list:
        result_list = sorted(result_list, key=lambda x: x[1])
        result_list[0][1] = result_list[0][1] - np.sum(np.arange(1, num_city))
        print(f"The searching result of A* when number of city is {num_city}:")
        print(result_list[0])
    else:
        print(f"The searching result of A* when number of city is {num_city}:")
        print("Failed to get the way!")