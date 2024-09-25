import random
import timeit
import pandas as pd


# Линейный поиск
def linear_search(arr, x):
    iterations = 0
    num_of_comp = 0
    position = 0
    i = 0
    n = len(arr) - 1

    while i <= n and arr[i] != x:
        iterations += 1
        num_of_comp += 1
        i = i + 1

        if i < n:
            position = i

    if i == n + 1:
        position = -1

    return position, iterations, num_of_comp


# Линейный поиск (с барьером)
def linear_search_barrier(arr, x):
    iterations = 0
    num_of_comp = 0
    position = 0
    i = 0
    n = len(arr) - 1

    arr.append(x)
    while arr[i] != x:
        iterations += 1
        num_of_comp += 1
        i = i + 1

        if i < n:
            position = i

        if i == n:
            position = -1

    return position, iterations, num_of_comp


# Бинарный поиск.
def binary_search(arr, x):
    position = 0
    num_of_comp = 0
    iterations = 0
    n = len(arr)
    left = 1
    right = n

    while left < right:
        iterations += 1
        m = (left + right) // 2
        if x == arr[m]:
            position = m
            num_of_comp += 1
            break
        if x > arr[m]:
            left = m + 1
            num_of_comp += 1
        if x < arr[m]:
            num_of_comp += 1
            right = m

    return position, iterations, num_of_comp


# Генерация массива.
def generate_array(size):
    arr = list(range(1, size + 1))
    random.shuffle(arr)
    return arr


# Размеры массивов для тестирования.
sizes = [100, 500, 1000, 3000, 10000]


# Задание 1
def task_1(x):
    for size in sizes:
        arr1 = generate_array(size)
        arr2 = generate_array(size)
        arr3 = generate_array(size)

        pos1, iters1, comps1 = linear_search(arr1, x)
        pos2, iters2, comps2 = linear_search(arr2, x)
        pos3, iters3, comps3 = linear_search(arr3, x)

        time1 = timeit.timeit(lambda: linear_search(arr1, x), number=1)
        time2 = timeit.timeit(lambda: linear_search(arr2, x), number=1)
        time3 = timeit.timeit(lambda: linear_search(arr3, x), number=1)

        print("-" * 20)
        print("Кол-во элементов:", size)
        print("Массив 1")
        print("Время поиска:", time1)
        print("Сравнений:", comps1)
        print("-" * 20)
        print("Массив 2")
        print("Время поиска:", time2)
        print("Сравнений:", comps2)
        print("-" * 20)
        print("Массив 3")
        print("Время поиска:", time3)
        print("Сравнений:", comps3)


# Задание 2.
def task_2(x):
    arr = sorted(generate_array(200))

    posl, itersl, compsl = linear_search(arr, x)
    posb, itersb, compsb = binary_search(arr, x)

    timel = timeit.timeit(lambda: linear_search(arr, x), number=3)
    timeb = timeit.timeit(lambda: binary_search(arr, x), number=3)

    # Результаты.
    results = {
        "linear": {
            "Element": x,
            "Iterations": itersl,
            "Comparisons": compsl,
            "Time": timel
        },
        "binary": {
            "Element": x,
            "Iterations": itersb,
            "Comparisons": compsb,
            "Time": timeb
        }
    }

    df = pd.DataFrame.from_dict(results)
    return df


# Задание 3.
def task_3(size, x):
    arr = generate_array(size)

    poswb, iterswb, compswb = linear_search(arr, x)
    posb, itersb, compsb = linear_search_barrier(arr, x)

    timel = timeit.timeit(lambda: linear_search(arr, x), number=1)
    timelb = timeit.timeit(lambda: linear_search_barrier(arr, x), number=1)

    results = {
        "base": {
            "Size": size,
            "Element": x,
            "Position": poswb,
            "Iterations": iterswb,
            "Comparisons": compswb,
            "Time": timel
        },
        "barrier": {
            "Size": size,
            "Element": x,
            "Position": posb,
            "Iterations": itersb,
            "Comparisons": compsb,
            "Time": timelb
        }
    }

    df = pd.DataFrame.from_dict(results)
    return df


# print(task_1(10))
# print(task_2(188))
print(task_3(100, 200))
