import numpy as np
import random


def printM(matrix):
    print(f"{divider}")
    for _ in range(m):
        print(matrix[_][1:], end="")
        print(f" - Sum = {matrix[_][0]}")


n = int(input("Введите N: "))
m = int(input("Введите M: "))
x = int(input("Нижняя граница: "))
y = int(input("Верхняя граница: "))

T = np.zeros((m, n), dtype=int).tolist()

divider = "----" * (n + 3)

for row in T:
    summ = 0
    for i in range(len(row)):
        row[i] = random.randint(x, y)
        summ += row[i]
    row.insert(0, summ)

T_sorted_1 = sorted(T, reverse=True)
T_sorted_2 = sorted(T)


def rasp(matrix):
    load = [0 for _ in range(n)]
    sum_of = [0 for _ in range(n)]
    for row in matrix:
        print(f"{divider}")
        print(f"Row = {row[1:]}")
        for j in range(n):
            sum_of[j] = load[j] + row[j + 1]
        print(f"Сумма = {sum_of}")
        min_ind = sum_of.index(min(sum_of))
        load[min_ind] += row[min_ind + 1]
        print(f"Нагрузка = {load}")

    return max(load)


print(f"{divider}\nНе отсортированная")
printM(T)
X = rasp(T)

print(f"{divider}\nПо возрастанию")
printM(T_sorted_2)
X_sorted_as = rasp(T_sorted_2)

print(f"{divider}\nПо убыванию")
printM(T_sorted_1)
X_sorted_des = rasp(T_sorted_1)

print(f"{divider}")
print(f"Итоговая нагрузка для неотсорт.: {X}")
print(f"Для отсортированной по убыванию: {X_sorted_as}")
print(f"Для отсортированной по возрастанию: {X_sorted_des}")
