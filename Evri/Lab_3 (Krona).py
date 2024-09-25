from random import randint  # Импортируем рандомайзер
from Lab_1 import *  # Импортируем метод критического пути из первой лабораторной


# Первый шаг метода Крона
def FirstStep(t, n):
    proc = [[] for _ in range(n)]
    for task in t:
        i = randint(0, n - 1)
        proc[i].append(task)
    return proc


# Второй шаг метода Крона
def SecondStep(proc):
    load = []
    for item in proc:
        load.append(sum(item))
    max_load = load.index(max(load))
    min_load = load.index(min(load))
    d = max(load) - min(load)

    while min(proc[max_load]) < d:
        temp = min(proc[max_load])
        proc[max_load].pop(proc[max_load].index(temp))
        proc[min_load].append(temp)
        load = []
        for item in proc:
            load.append(sum(item))
        max_load = load.index(max(load))
        min_load = load.index(min(load))
        d = max(load) - min(load)

    return load


# Ввод начальных значений
M = int(input("Кол-во задач M: "))
N = int(input("Кол-во процессоров N: "))
T1 = int(input("Нижняя граница: "))
T2 = int(input("Верхняя граница: "))

# Заполнение списка задач
T = [randint(T1, T2) for _ in range(M)]
T_sorted = sorted(T, reverse=True)

# Вывод задач
print(f"Неотсорт - {T}", f"Отсорт - {T_sorted}", sep="\n")


# Функция вывода матрицы загрузок
def print_load(p):
    i = 1
    for item in p:
        print(f"p{i} = {item}")
        i += 1


# Вывод матриц загрузок
print("Шаг 1")
p = FirstStep(T, N)
print(f"Not sorted ----------")
print_load(p)
p2 = FirstStep(T_sorted, N)
print(f"Sorted --------------")
print_load(p2)

input("Нажмите Enter чтобы продолжить...")
print("----------------------")

# Вывод ответа
print("Решение для неотсортированной")
print(f"Крон - {SecondStep(p)} === {max(SecondStep(p))}")
print(f"Мод Крон - {SecondStep(cr_way(T, N))} === {max(SecondStep(cr_way(T, N)))}")

print("Решение для отсортированной")
print(f"Крон - {SecondStep(p2)} === {max(SecondStep(p2))}")
print(f"Мод Крон - {SecondStep(cr_way(T_sorted, N))}  === {max(SecondStep(cr_way(T_sorted, N)))}")
