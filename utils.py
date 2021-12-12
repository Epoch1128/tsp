import numpy as np
from matplotlib import pyplot as plt
from math import sqrt


def cal_L2_distance(point_a, point_b, dim=2):
    """
    Calculate the L2 distance between A and B
    """
    dis = 0
    for i in range(dim):
        dis = dis + (point_a[i] - point_b[i]) ** 2
    return sqrt(dis)


def map_to_graph(map, num_city):
    """
    Convert the map(with coordinates (x, y)) to distance graph
    """
    graph = np.zeros((num_city, num_city))
    for i in range(num_city):
        for j in range(i + 1, num_city):
            graph[i][j] = cal_L2_distance(map[i], map[j])

    return graph + graph.transpose()


def get_map(coordinate, rank):
    plt.figure()
    for item in coordinate:
        plt.scatter(item[0], item[1])
    plt.plot(coordinate[:,0], coordinate[:,1])
    plt.plot([coordinate[-1][0], coordinate[0][0]], [coordinate[-1][1], coordinate[0][1]])
    plt.savefig("SA_result//best_traj_{}.jpg".format(rank))
