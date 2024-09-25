import numpy as np
import Lab_7_func as L7
import random
import networkx as nx
import matplotlib.pyplot as plt

matrix_size = 10
lower_limit = 10
upper_limit = 20
population_size = 100
max_repeats = 100
crossover_prob = 0.7
mutation_prob = 0.7
start_poss = 8

with open('lab_7_ways.txt', 'w'):
    pass
# matrix = L7.create_symmetric_path_matrix(matrix_size, lower_limit, upper_limit)
# test = L7.GeneticAlg(matrix, population_size, max_repeats, crossover_prob, mutation_prob, start_poss)
# test.run()

matrix = np.array([[0, 13, 14, 13, 14, 15, 16, 18, 13, 14],
                   [13, 0, 14, 15, 14, 16, 11, 15, 10, 18],
                   [14, 14, 0, 16, 18, 19, 14, 15, 12, 12],
                   [13, 15, 16, 0, 19, 10, 15, 14, 16, 11],
                   [14, 14, 18, 19, 0, 14, 16, 17, 18, 10],
                   [15, 16, 19, 10, 14, 0, 12, 16, 16, 12],
                   [16, 11, 14, 15, 16, 12, 0, 11, 13, 15],
                   [18, 15, 15, 14, 17, 16, 11, 0, 19, 17],
                   [13, 10, 12, 16, 18, 16, 13, 19, 0, 19],
                   [14, 18, 12, 11, 10, 12, 15, 17, 19, 0]])

test = L7.GeneticAlg(matrix, population_size, max_repeats, crossover_prob, mutation_prob, start_poss)
test.run()

# Инициализация графа
G = nx.DiGraph()

# Получение количества вершин
num_nodes = matrix.shape[0]

# Добавление рёбер с весами в граф
for i in range(num_nodes):
    for j in range(i + 1, num_nodes):
        if matrix[i, j] != 0:
            G.add_edge(i, j, weight=matrix[i, j])

# Позиционирование вершин графа
pos = nx.circular_layout(G)

# Отрисовка всех рёбер графа
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', arrowstyle='-')

best_path = test.best_individual.genes
path_edges = [(best_path[i] - 1, best_path[i + 1] - 1) for i in range(len(best_path) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, arrowstyle='-|>', arrowsize=20)

# Отрисовка вершин и их меток
node_colors = ['lightblue'] * num_nodes
node_colors[start_poss - 1] = 'orange'  # Перекрашиваем вершину с номером 3 (индекс 2) в оранжевый цвет

nx.draw_networkx_nodes(G, pos, node_color=node_colors)
nx.draw_networkx_labels(G, pos, labels={i: f'{i + 1}' for i in range(num_nodes)})

# Отображение графа
plt.show()
