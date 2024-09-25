import random
import copy

# Вводим данные.
N = int(input("Введите N -> "))
M = int(input("Введите M -> "))
T1 = int(input("Введите T1 -> "))
T2 = int(input("Введите T2 -> "))

matrix_rand = [random.sample(range(T1, T2), N) for j in range(M)]


# Сортировка матрицы.
def sorter(arr, reverse):
    return sorted(copy.deepcopy(arr), key=lambda row: sum(row), reverse=reverse)


# Печать матрицы.
def matrix_print(arr):
    c = copy.deepcopy(arr)
    for s in c:
        print(s)


# Печать словаря.
def dict_print(dic):
    for key, value in dic.items():
        print(f"{key}:", value)


# Решение минимаксной задачи с заданной степенью критерия.
def free_schedule_modified(sorted_matrix, degree=2):
    sorted_matrix = copy.deepcopy(sorted_matrix)

    # Словарь процессоров.
    procs_dict = {n: [] for n in range(N)}

    for i in range(M):

        # Словарь с информацией о суммах по строкам.
        row_sums = {row: 0 for row in range(N)}

        # Считаем суммы в текущей строке.
        for j in range(N):
            row_sum = (sorted_matrix[i][j] + sum(procs_dict[j])) ** degree if len(procs_dict[j]) > 0 else \
                sorted_matrix[i][j] ** degree
            for k in range(N):
                if k != j:
                    row_sum += sum(procs_dict[k]) ** degree
            row_sums[j] = row_sum

        # Минимальная сумма в текущей строке.
        min_row_sum = min(list(row_sums.values()))

        # Назначаем на процессор задание, на котором была найдена минимальная сумма.
        for ind, cur_sum in row_sums.items():
            if cur_sum == min_row_sum:
                procs_dict[ind].append(sorted_matrix[i][ind])

        # Вывод текущего состояния процессоров.
        print("-" * 10)
        print(f"  Шаг {i + 1}  ")
        print("-" * 10)
        dict_print(procs_dict)

        # Вывод сумм строк.
        print(f"Суммы по строке {i + 1}")
        dict_print(row_sums)

    # Вычисляем cуммы по процессорам и максимальную нагрузку.
    sums = [sum(procs_dict[index]) for index in procs_dict]
    max_sum = max(sums)

    # Выводим результаты.
    print("-" * 50)
    print("Таблица заданий, назначенных на процессоры")
    print("-" * 50)
    dict_print(procs_dict)
    print("-" * 50)
    print("Суммы по процессорам: ", sums)
    print("Максимальная нагрузка: ", max_sum)


# Сортированные копии матриц.
sorted_up = sorter(matrix_rand, True)
sorted_down = sorter(matrix_rand, False)


# Утилита для вывода.
def display_result(title, sort_type, matrix, criteria):
    print("-" * 60)
    print(title)
    print(sort_type)
    print("")
    print("Матрица")
    matrix_print(matrix)
    free_schedule_modified(matrix, criteria)


# Меню работы с программой.
while True:
    print("-" * 100)
    print("Решение минимаксной задачи алгоритмом Плотникова с квадратичным (заданной степени) критерием.")
    print("-" * 100)
    choose = int(input("Квадратичный критерий без сортировки (1)\n"
                       "Квадратичный критерий по убыванию (2)\n"
                       "Квадратичный критерий по возрастанию (3)\n"
                       "Кубический критерий без сортировки (4)\n"
                       "Кубический критерий по убыванию (5)\n"
                       "Кубический критерий по возрастанию (6)\n"
                       "Выход из меню (что-либо другое)\n"
                       ))
    if choose == 1:
        display_result("Квадратичный критерий", "По возрастанию", matrix_rand, 2)
    elif choose == 2:
        display_result("Квадратичный критерий", "По убыванию", sorted_up, 2)
    elif choose == 3:
        display_result("Квадратичный критерий", "По возрастанию", sorted_down, 2)
    elif choose == 4:
        display_result("Кубический критерий", "Без сортировки", matrix_rand, 3)
    elif choose == 5:
        display_result("Кубический критерий", "По убыванию", sorted_up, 3)
    elif choose == 6:
        display_result("Кубический критерий", "По возрастанию", sorted_down, 3)
    else:
        exit()
