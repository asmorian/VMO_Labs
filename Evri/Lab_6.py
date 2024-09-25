import random


def printM(matrix):
    for _ in range(m):
        print(matrix[_])


def cr_way(tasks, num_proc):
    proc = [[] for _ in range(num_proc)]
    load = [0 for _ in range(num_proc)]

    for task in tasks:
        min_index = load.index(min(load))
        proc[min_index].append(task)
        load[min_index] += task

    return proc


def rasp(matrix, proc_num):
    load = [0 for _ in range(proc_num)]
    sum_of = [0 for _ in range(proc_num)]
    for item in matrix:
        for j in range(proc_num):
            sum_of[j] = load[j] + item[j + 1]
        min_ind = sum_of.index(min(sum_of))
        load[min_ind] += item[min_ind + 1]

    return load


def six(matrix):
    min_matrix = []
    proc_num = len(matrix[0])
    for item in matrix:
        min_matrix.append(min(item))
    limit = sum(min_matrix) / proc_num
    proc = [[] for _ in range(proc_num)]
    load = [0 for _ in range(proc_num)]
    sum_of = [0 for _ in range(proc_num)]
    print(f"Limit = {limit}")

    i = 0
    while True:
        item = matrix[i]
        min_value = min(item)
        min_index = item.index(min_value)

        if load[min_index] + min_value >= limit:
            break

        proc[min_index].append(min_value)
        load[min_index] += min_value
        i += 1
    print(f"Лимит достигнут при загрузке {load} в строке {i}")

    for item in matrix[i:]:
        for j in range(proc_num):
            sum_of[j] = load[j] + item[j]
        mindex = sum_of.index(min(sum_of))
        load[mindex] += item[mindex]
        proc[mindex].append(item[mindex])

    print(load, "---", proc)


n = int(input("Введите N: "))
m = int(input("Введите M: "))
x = int(input("Нижняя граница: "))
y = int(input("Верхняя граница: "))

mat = [[] for _ in range(m)]
for row in mat:
    for _ in range(n):
        row.append(random.randint(x, y))

printM(mat)
six(mat)
