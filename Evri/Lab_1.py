import random


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


def cr_way(tasks, num_proc):
    proc = [[] for i in range(num_proc)]
    load = [0 for i in range(num_proc)]

    for task in tasks:
        min_index = load.index(min(load))
        proc[min_index].append(task)
        load[min_index] += task

    return proc


def half_division(used_matrix):
    n = len(used_matrix[0])
    if n % 2 == 0:
        processors = [0] * n
        t = []
        for i in range(len(used_matrix)):
            t.append(used_matrix[i][0])
        p_AB = [[], []]
        for index, item in enumerate(t):
            p_A = sum(t[i] for i in p_AB[0])
            p_B = sum(t[i] for i in p_AB[1])
            if p_A > p_B:
                p_AB[1].append(index)
            else:
                p_AB[0].append(index)

        print("----------------------------\np_A:", p_AB[0],
              "\np_B: ", p_AB[1])
        for index in p_AB[0]:
            processors[processors.index(min(processors[:int(n / 2)]))] += t[index]
        for index in p_AB[1]:
            processors[processors.index(min(processors[int(n / 2):]))] += t[index]
        return processors
    else:
        print("Кол-во процессоров должно быть чётным")


def half_step(t):
    p_1 = [0]
    p_2 = [0]
    for item in t:
        if sum(t[i][1] for i in p_1) > sum(t[i][1] for i in p_2):
            p_2.append(item)
        else:
            p_1.append(item)
    return p_1, p_2

#
# task_string_list_range = input("Нижний и верхний предел T: ").split(", ")
# task_list_range = map(int, task_string_list_range)
# task_list_range = list(task_list_range)
#
# task_list_size = int(input("Кол-во T: "))
# task_list = []
# for i in range(task_list_size):
#     task_list.append(random.randint(task_list_range[0], task_list_range[1]))
# print("T = ", task_list)
# proc_num = int(input("Введите кол-во процессоров N: "))
#
# matrix = []
# for i in range(proc_num):
#     matrix.append(task_list)
# rotated = tuple(zip(*matrix[::-1]))
#
# sort_rotated = sorted(rotated)
# rev_sort_rotated = list(reversed(sort_rotated))
#
# print("Неотсортированная матрица")
# for i in range(len(rotated)):
#     print(rotated[i])
# print("----------------------------\nОтсортированная по возрастанию")
# for i in range(len(sort_rotated)):
#     print(sort_rotated[i])
# print("----------------------------\nОтсортированная по убыванию")
# for i in range(len(rev_sort_rotated)):
#     print(rev_sort_rotated[i])
#
# print("----------------------------",
#       "\nДля неотсортированной матрицы: ", crit_way(rotated),
#       "\nДля сортированной в порядке возрастания: ", crit_way(sort_rotated),
#       "\nДля сортированной в порядке убывания: ", crit_way(rev_sort_rotated),
#       "\nМетодом половинного деления: ", half_division(rev_sort_rotated))
