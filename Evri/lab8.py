import random
import copy

# Вводим исходные данные.
n = int(input("Введите N -> "))
m = int(input("Введите M -> "))
t1 = int(input("Введите T1 -> "))
t2 = int(input("Введите T2 -> "))
inf_num = int(input("Количество ∞ в таблице ограничений: "))


# Печать матрицы.
def matrix_print(arr):
    c = copy.deepcopy(arr)
    for s in c:
        print(s)


# Печать словаря.
def dict_print(dic):
    for key, value in dic.items():
        print(f"{key}:", value)


# Сортировка таблицы ограничений c разными параметрами учета бесконечностей.
# inf_mode:
# --no_changes = сортировка по убыванию без изменений.
# --inf_include = c учетом бесконечности.
# --inf_in_str = c учетом количества бесконечностей в строке.
def sorter(pl, inf_mode, reverse=True):
    if inf_mode == "no_changes":
        sorted_pl = sorted(copy.deepcopy(pl),
                           key=lambda row: list(set(filter(lambda x: x != "inf", row)))[0],
                           reverse=reverse)
        t = [[sorted_pl[i][j] for j in range(len(sorted_pl[i])) if sorted_pl[i][j] != "inf"] for i in
             range(len(sorted_pl))]
        t = list(map(lambda x: list(set(x))[0], list(sorted(t, reverse=reverse))))
        return sorted_pl, t

    if inf_mode == "inf_include":
        l_infs = []
        l_noinfs = []
        for i in range(len(pl)):
            if "inf" in pl[i]:
                l_infs.append(pl[i])
            else:
                l_noinfs.append(pl[i])
        sorted_pl_infs = sorted(l_infs,
                                key=lambda row: list(set(filter(lambda x: x != "inf", row)))[0],
                                reverse=reverse)
        sorted_pl_noinfs = sorted(l_noinfs, key=lambda row: sum(row), reverse=reverse)
        sorted_pl = sorted_pl_infs + sorted_pl_noinfs
        t = [[sorted_pl[i][j] for j in range(len(sorted_pl[i])) if sorted_pl[i][j] != "inf"] for i in
             range(len(sorted_pl))]
        t = list(map(lambda x: list(set(x))[0], t))
        return sorted_pl, t

    if inf_mode == "inf_in_str":
        l_infs = []
        l_noinfs = []

        # Разделение элементов на содержащие "inf" и не содержащие
        for item in pl:
            if "inf" in item:
                l_infs.append(item)
            else:
                l_noinfs.append(item)

        # Функция для сортировки списков с "inf"
        def inf_sort_key(row):
            inf_count = row.count("inf")
            sum_without_inf = sum([x for x in row if x != "inf"])
            return (inf_count, sum_without_inf)

        # Сортировка
        sorted_pl_infs = sorted(l_infs, key=inf_sort_key, reverse=reverse)
        sorted_pl_noinfs = sorted(l_noinfs, key=lambda row: sum(row), reverse=reverse)

        # Объединение отсортированных списков
        sorted_pl = sorted_pl_infs + sorted_pl_noinfs

        # Удаление "inf" и преобразование
        t = [[sorted_pl[i][j] for j in range(len(sorted_pl[i])) if sorted_pl[i][j] != "inf"] for i in
             range(len(sorted_pl))]
        t = list(map(lambda x: list(set(x))[0], t))

        return sorted_pl, t


# Начальный список заданий.
tasks = [random.randint(t1, t2) for _ in range(m)]

# Шаблон таблицы ограничений процессоров.
procs_limits = [[tasks[i]] * n for i in range(m)]

# Рандомно распределяем inf_num ограничений (бесконечностей) по procs_limits.
infs_count = 0
while infs_count < inf_num:
    row_i = random.randint(0, m - 1)
    col_i = random.randint(0, n - 1)
    if procs_limits[row_i][col_i] != "inf":
        infs_row_count = procs_limits[row_i].count("inf")
        if infs_row_count == n - 1:
            continue
        procs_limits[row_i][col_i] = "inf"
        infs_count += 1

# -----------------------
#  ПРИМЕР ИЗ МЕТОДИЧКИ.
# -----------------------
# procs_limits = [
#     [15, "inf", "inf", 15],
#     [12, "inf", 12, 12],
#     [11, 11, "inf", 11],
#     [10, 10, 10, 10],
#     ["inf", "inf", 8, 8],
#     [7, 7, 7, 7],
#     [6, 6, "inf", "inf"],
#     [4, 4, "inf", "inf"],
#     ["inf", 4, "inf", "inf"],
#     [3, 3, 3, 3]
# ]
# tasks = [15, 12, 11, 10, 8, 7, 6, 4, 4, 3]


# Модицификация алгоритма критического пути c учетом
# бесконечного времени выполнения заданий.
def cmp_inf(pl, t, N, M):
    print("-" * 50)
    print("Сортированная матрица процессорных ограничений")
    matrix_print(pl)
    print("-" * 60)

    print("Список заданий:", t)
    print("-" * 60)

    table = [0 for _ in range(N)]
    procs_state = {proc: [] for proc in range(N)}

    # проходимся по всем строкам таблицы ограничений.
    for i in range(M):
        # находим процессор с минимальной нагрузкой.
        min_load_num = table.index(min(table))

        # если на процессоре с мин.нагрузкой бесконечное время вып. задания
        if pl[i][min_load_num] == "inf":
            # ищем доступные процессоры.
            indexes = [j for j in range(len(pl[i])) if pl[i][j] != "inf"]
            # ищем нагрузки на доступных процессорах.
            possible_pos = {ind: 0 for ind in indexes}
            for ind in indexes:
                possible_pos[ind] += table[ind]
            # если среди доступных процессоров есть несколько свободных
            if min(list(possible_pos.values())) == 0:
                possible_min = 0
                for val in possible_pos:
                    if pl[i][val] != "inf" and possible_pos[val] == 0:
                        possible_min = val
                        break
                table[possible_min] += t[i]
                procs_state[possible_min].append(t[i])
            # в ином случае назначаем на процессор, имеющий мин.нагрузку среди всех доступных
            else:
                new_min = table.index(min(list(possible_pos.values())))
                table[new_min] += t[i]
                procs_state[new_min].append(t[i])
        # если процессор с мин.нагрузкой доступен для назначения задания.
        else:
            table[min_load_num] += t[i]
            procs_state[min_load_num].append(t[i])

        print("-" * 10)
        print(f"  Шаг {i + 1}  ")
        print("-" * 10)
        dict_print(procs_state)

    print("-" * 30)
    print(f"Максимальная нагрузка: max({table}) = {max(table)}")


# Меню работы с программой.
while True:
    print("-" * 50)
    print("Модификации алгоритма критического пути")
    print("-" * 50)
    choose = int(input("Сортировка без изменений (1)\n"
                       "Сортировка c учетом бесконечностей (2)\n"
                       "Сортировка с учетом кол-ва бесконечностей в строке (3)\n"
                       "Выход из меню (4)\n"
                       ))
    if choose == 1:
        procs_limits_sorted, tasks = sorter(procs_limits, "no_changes")
        print("-" * 50)
        print("Начальная матрица ограничений")
        matrix_print(procs_limits)
        cmp_inf(procs_limits_sorted, tasks, n, m)
    elif choose == 2:
        procs_limits_sorted, tasks = sorter(procs_limits, "inf_include")
        print("-" * 50)
        print("Начальная матрица ограничений")
        matrix_print(procs_limits)
        cmp_inf(procs_limits_sorted, tasks, n, m)
    elif choose == 3:
        procs_limits_sorted, tasks = sorter(procs_limits, "inf_in_str")
        print("-" * 50)
        print("Начальная матрица ограничений")
        matrix_print(procs_limits)
        cmp_inf(procs_limits_sorted, tasks, n, m)
    else:
        exit()
