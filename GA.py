import numpy as np
import random
from config import *
from utils import map_to_graph
from tqdm import tqdm


def fitness(graph, seq):
    if len(seq) != graph.shape[0]:
        raise ValueError("The input seqence or graph is illegal!")

    cost = 0
    for i in range(len(seq)):
        cost = cost + graph[seq[i]][seq[(i + 1) % len(seq)]]

    return 1 / cost


# cross evolution
def cross(x, y):
    """
    Cross inheritance
    """

    def conflict_index(gene, begin, end):
        new_list = []
        for i, item in enumerate(gene):
            if item not in new_list:
                new_list.append(item)
            else:
                if i >= begin & i < end:
                    in_index = i
                    out_index = new_list.index(item)
                else:
                    in_index = new_list.index(item)
                    out_index = i
                return in_index, out_index
        return None

    if len(x) != len(y):
        raise ValueError("The gene length is illegal!")
    start = np.random.randint(0, len(x))
    finish = np.random.randint(start, len(x) + 1)
    for i in range(start, finish):
        temp = x[i]
        x[i] = y[i]
        y[i] = temp
    index = conflict_index(x, start, finish)
    while index != None:
        x[index[1]] = y[index[0]]
        index = conflict_index(x, start, finish)
    index = conflict_index(y, start, finish)
    while index != None:
        y[index[1]] = x[index[0]]
        index = conflict_index(y, start, finish)
    return x, y


def mutation(x):
    """
    Gene mutation: exchange two elements in the gene-seq
    """
    start = np.random.randint(0, len(x) - 1)
    finish = np.random.randint(start, len(x))
    temp = x[start]
    x[start] = x[finish]
    x[finish] = temp
    return x


def print_gene_list(gene, name):
    print("\t" + name + ":")
    for item in gene:
        print("\t\t{}".format(item))


def select(gene_list):
    score = []
    new_gene_list = []
    sum = 0
    for item in gene_list:
        sum = sum + item[1]

    for i, item in enumerate(gene_list):
        if i != 0:
            score.append(item[1] / sum + score[i - 1])
        else:
            score.append(item[1] / sum)

    for _ in range(len(gene_list)):
        selection = np.random.rand()
        tag = 0
        for i in range(1, len(score)):
            if selection >= score[i - 1] and selection < score[i]:
                tag = i - 1
        new_gene_list.append(gene_list[tag])
    return sorted(new_gene_list, key=lambda x: x[1], reverse=True)


def GA_evolution(num_of_city, maps, pc, pm, n):
    # Initialization
    gene = []
    graph = map_to_graph(maps, num_of_city)
    for _ in range(n):
        sequence = list(np.random.permutation(range(num_of_city)))
        # for debugging
        # sequence = [i for i in range(num_of_city)]
        gene.append([sequence, fitness(graph, sequence)])
    # print_gene_list(sorted(gene, key=lambda x: x[1], reverse=True), "origin")
    # evolution
    gene = sorted(gene, key=lambda x: x[1], reverse=True)
    for iter_time in range(50):
        # print("Epoch {}:".format(iter_time))
        # select
        cross_score = int(num_of_city * pc / 2)
        new_gene = []
        gene = select(gene)
        rand_sampler = random.sample(range(num_of_city - cross_score * 2, num_of_city), cross_score * 2)
        # print_gene_list(gene, "after select")

        # cross
        new_gene.extend(gene[0: num_of_city - cross_score * 2])
        # print_gene_list(sorted(new_gene, key=lambda x: x[1], reverse=True), "before cross")
        for i in range(cross_score):
            sons = cross(gene[rand_sampler[i]][0], gene[rand_sampler[i + cross_score]][0])
            new_gene.append([sons[0], fitness(graph, sons[0])])
            new_gene.append([sons[1], fitness(graph, sons[1])])
        # print_gene_list(sorted(new_gene, key=lambda x: x[1], reverse=True), "after cross")

        # mutation
        for item in new_gene:
            mut_score = np.random.rand()
            if mut_score < pm:
                item[0] = mutation(item[0])
                item[1] = fitness(graph, item[0])

        gene = sorted(new_gene, key=lambda x: x[1], reverse=True)
        # print_gene_list(gene, "after mutation")

    return gene[0][0], 1 / gene[0][1]


if __name__ == '__main__':
    result_list = []
    for _ in tqdm(range(1000)):
        result_list.append(GA_evolution(num_city, map, Pc, Pm, N))

    min_index = result_list.index(min(result_list, key=lambda x: x[1]))
    print(result_list[min_index])