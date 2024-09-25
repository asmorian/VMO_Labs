import random
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy

n = int(input("Введите количество вершин: "))
t1 = int(input("Введите минимальное значение веса: "))
t2 = int(input("Введите максимальное значение веса: "))
start_vertex = int(input("Введите начальную вершину: "))
z = int(input("Введите количество особей в начальной популяции: "))
k = int(input("Введите количество повторений лучших особей: "))
pk = int(input("Введите вероятность кроссовера в процентах: "))
pm = int(input("Введите вероятность мутации в процентах: "))

INF = t2 + 1

graph = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        t = random.randint(t1, t2)
        graph[i][j] = t
        graph[j][i] = t

G = nx.Graph()
for i in range(n):
    G.add_node(i)

edges_label = {}
for i in range(n):
    for j in range(i + 1, n):
        if i != j:
            G.add_edge(i, j, weight=graph[i][j])
            edges_label[(i, j)] = graph[i][j]

for row in graph:
    print(row)

# Жадный алгоритм
def get_min(visited: list, graph_row: list) -> int:
    min_ = INF
    vertex = 0
    for vertex_index, number in enumerate(graph_row):
        if (number != 0 and
                number < min_ and
                not visited[vertex_index]):
            min_ = number
            vertex = vertex_index

    return vertex

visited = [0 for _ in range(n)]
visited[start_vertex] = 1
current_vertex = start_vertex
route = [start_vertex]
while 0 in visited:
    row = graph[current_vertex]
    current_vertex = get_min(visited, row)
    visited[current_vertex] = 1
    route.append(current_vertex)
route.append(start_vertex)

red_edges = []
for i in range(n):
    weight = graph[route[i]][route[i + 1]]
    red_edges.append(
        (route[i], route[i + 1])
    )

first_generation = []
for _ in range(z):
    l = [start_vertex]
    while True:
        number = random.randint(0, n - 1)
        if number not in l:
            l.append(number)
        if len(l) == n:
            break
    l.append(start_vertex)
    first_generation.append(l)

generations = [first_generation]

def get_max_load(route):
    global n
    load = 0
    for i in range(n):
        weight = graph[route[i]][route[i + 1]]
        load += weight
    return load

def mutation(p):
    global n
    new_p = deepcopy(p)
    index1 = random.randint(1, n - 2)
    while True:
        index2 = random.randint(1, n - 2)
        if index1 != index2:
            break
    tmp = new_p[index1]
    new_p[index1] = new_p[index2]
    new_p[index2] = tmp
    print("Мутировали в генах", index1 + 1, index2 + 1)
    return new_p

def crossover(o1: list, o2: list, div: int):
    o1_new = deepcopy(o1[:div])
    o2_new = deepcopy(o2[:div])
    for elem in o2:
        if elem not in o1_new:
            o1_new.append(elem)
    for elem in o1:
        if elem not in o2_new:
            o2_new.append(elem)
    o1_new.append(o1[0])
    o2_new.append(o2[0])
    return deepcopy(o1_new), deepcopy(o2_new)

def get_best_p(o1, generation):
    global n, pk, pm
    o2 = random.randint(0, z - 1)
    while True:
        o2 = random.randint(0, z - 1)
        if o1 != o2:
            break

    print(f"Выбраны особи {o1 + 1} {o2 + 1}")
    o1 = generation[o1]
    o2 = generation[o2]
    print("родитель 1:", o1, get_max_load(o1))
    print("родитель 2 :", o2, get_max_load(o2))
    if random.choices([True, False], weights=[pk, 100 - pk])[0]:
        div = random.randint(2, n - 3)
        print(f"Разделитель {div}")
        p1, p2 = crossover(o1, o2, div)
    else:
        p1, p2 = deepcopy(o1), deepcopy(o2)

    print("Потомок 1:", p1, "результат:", get_max_load(p1))
    print("Потомок 2:", p2, "результат:", get_max_load(p2))
    if random.choices([True, False], weights=[pm, 100 - pm])[0]:
        p1 = mutation(p1)
        print("Потомок 1 после мутации:", p1, "результат:", get_max_load(p1))

    if random.choices([True, False], weights=[pm, 100 - pm])[0]:
        p2 = mutation(p2)
        print("Потомок 2 после мутации:", p2, "результат:", get_max_load(p2))

    p2_load = get_max_load(p2)
    p1_load = get_max_load(p1)

    if p1_load >= p2_load:
        return p2, p2_load

    return p1, p1_load

def output_generation(generation):
    print("Особи в поколении:")
    global n
    for o in generation:
        print(o, "результат:", get_max_load(o))

def create_generation(generation):
    new_generation = []
    for i, o in enumerate(generation):
        print(f"Для {i + 1} особи")
        p, p_load = get_best_p(i, generation)
        o_load = get_max_load(o)
        if o_load < p_load:
            new_generation.append(deepcopy(o))
        else:
            new_generation.append(deepcopy(p))
    return new_generation

index = 0

while True:
    current_generation = generations[index]
    print(index + 1, "поколение")
    output_generation(current_generation)
    new_generation = create_generation(current_generation)
    generations.append(new_generation)
    index += 1

    if index >= k:
        check = []
        for generation in generations[-k:]:
            tmp = []
            for o in generation:
                max_load = get_max_load(o)
                tmp.append(max_load)
            check.append(min(tmp))

        min_check = min(check)
        if check.count(min_check) == k:
            break
output_generation(generations[-1])
print("Нашли за", index, "поколений")

gen = sorted(generations[-1], key=lambda o: get_max_load(o))
best_route = gen[0]
print("Генетический алгоритм(на 1 графе зеленым цветом): маршрут", best_route, "результат:", get_max_load(best_route))
#print("Жадный алгоритм(на 2 графе красным цветом): маршрут", route, "результат:", get_max_load(route))
green_edges = []
for i in range(n):
    green_edges.append(
        (best_route[i], best_route[i + 1])
    )
gen_options = {
    'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}
options = {
    'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}

plt.figure()
pos = nx.circular_layout(G)
pos2 = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_nodes(G, pos, nodelist=[start_vertex], node_color='purple')
nx.draw_networkx_edges(G, pos, edge_color='black', arrows=False)
#nx.draw_networkx_labels(G, pos2)
nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='green', arrows=True, **gen_options)
#nx.draw_networkx_edge_labels(G, pos2, edge_labels=edges_label)

#plt.figure()
#pos = nx.circular_layout(G)
#pos2 = nx.spring_layout(G)
#nx.draw_networkx_nodes(G, pos)
#nx.draw_networkx_nodes(G, pos, nodelist=[start_vertex], node_color='purple')
#nx.draw_networkx_edges(G, pos, edge_color='black', arrows=False)
#nx.draw_networkx_labels(G, pos2)
#nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', arrows=True, **options)
#nx.draw_networkx_edge_labels(G, pos2, edge_labels=edges_label)

plt.show()
