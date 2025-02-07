import random
import matplotlib.pyplot as plt


def crit_way(used_matrix):
    n = len(used_matrix[0])
    processors = [0] * n
    t = []
    for i in range(len(used_matrix)):
        t.append(used_matrix[i][0])

    while t:
        processors[processors.index(min(processors))] += t[0]
        t.pop(0)

    return processors


def crate_matrix(range_T, task_list_size, proc_num):
    task_string_list_range = range_T.split(", ")
    task_list_range = map(int, task_string_list_range)
    task_list_range = list(task_list_range)

    task_list = []
    for i in range(task_list_size):
        task_list.append(random.randint(task_list_range[0], task_list_range[1]))

    matrix = []
    for i in range(proc_num):
        matrix.append(task_list)

    rotated = tuple(zip(*matrix[::-1]))
    sort_rotated = sorted(rotated)
    rev_sort_rotated = list(reversed(sort_rotated))

    return [rotated, sort_rotated, rev_sort_rotated]


def create_mass(l, r, tls, pn):
    mass = []

    if not r:
        r = input("Введите нижний и верхний предел через запятую: ")
        tls = int(input("Введите кол-во задач: "))
        pn = int(input("Введите кол-во процессоров: "))

    for i in range(l):
        mass.append(crate_matrix(r, tls, pn))

    return mass


def solve(m):
    counter = [0, 0, 0]
    best_ever = 100 ** 10
    num = 0
    keeper = [0, 0, 0]
    for item in m:
        temp = [crit_way(item[0]), crit_way(item[1]), crit_way(item[2])]
        maxes = []
        for i in range(len(temp)):
            maxes.append(max(temp[i]))

        # print(f"{maxes} - {m.index(item)}")
        b = min(maxes)
        best = maxes.index(min(maxes))
        if b < best_ever:
            # print(best_ever)
            best_ever = b
            num = m.index(item)

        keeper[best] += b

        counter[best] += 1

    med = [0, 0, 0]
    for i in range(3):
        if counter[i] != 0:
            med[i] = keeper[i] / counter[i]

    return counter
    # , best_ever, num, med


def crate_graf(m):
    x_1 = []
    y_1 = []
    y_2 = []

    mass_ratio = []

    for i in range(len(m)):
        x_1.append(i + 1)
        y_1.append(m[i][0] + 5)
        y_2.append(m[i][1] - 5)

        if (m[i][1] - 5) != 0:
            ratio = (m[i][1] - 5) / (m[i][0] + 5)
        else:
            ratio = 100

        mass_ratio.append(ratio)

        print(f"{m[i][1] - 5} / {m[i][0] + 5} ~ {format(ratio, '.2f')}")

    print(f"Average = {format(sum(mass_ratio) / len(mass_ratio), '.2f')}")

    plt.plot(x_1, y_1, color='green', marker='o', markersize=3)
    plt.plot(x_1, y_2, color='purple', marker='o', markersize=3)
    plt.ylabel("Кол-во лучших")
    plt.xlabel("Номер теста")
    plt.show()


l = 100

# s, besty, numof, med = solve(create_mass(l))
# print(s, besty, numof, med)
#
# better = s.index(max(s))

# r = input("Введите нижний и верхний предел через запятую: ")
# tls = int(input("Введите кол-во задач: "))
# pn = int(input("Введите кол-во процессоров: "))
# number = int(input("Введите кол-во экспериментов: "))

mass = []
for i in range(50):
    x = solve(create_mass(l, r="10, 20", tls=11, pn=4))
    temp = [x[0], x[2]]
    mass.append(temp)

crate_graf(mass)
