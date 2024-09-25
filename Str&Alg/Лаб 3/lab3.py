import timeit
import random
import pandas as pd


def insertion_sort(mas):
    n = len(mas)
    iterations = 0
    comparisons = 0
    exchanges = 0
    for i in range(1, n):
        key = mas[i]
        j = i - 1
        iterations += 1
        while j >= 0 and key < mas[j]:
            comparisons += 1
            exchanges += 1
            mas[j + 1] = mas[j]
            j -= 1
        comparisons += 1
        mas[j + 1] = key
    return iterations, comparisons, exchanges


def selection_sort(mas):
    iterations = 0
    comparisons = 0
    exchanges = 0
    n = len(mas)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            iterations += 1
            if mas[j] < mas[min_idx]:
                comparisons += 1
                min_idx = j
            else:
                comparisons += 1
        exchanges += 1
        mas[i], mas[min_idx] = mas[min_idx], mas[i]
    return iterations, comparisons, exchanges


def bubble_sort(mas):
    n = len(mas)
    iterations = 0
    comparisons = 0
    exchanges = 0
    for i in range(n):
        for j in range(n - i - 1):
            iterations += 1
            if mas[j] > mas[j + 1]:
                comparisons += 1
                mas[j], mas[j + 1] = mas[j + 1], mas[j]
                exchanges += 1
            else:
                comparisons += 1
    return iterations, comparisons, exchanges


def quick_sort(mas):
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot = mas[(low + high) // 2]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while mas[i] < pivot:
                comparisons += 1
                i += 1
            j -= 1
            while mas[j] > pivot:
                comparisons += 1
                j -= 1
            if i >= j:
                return j
            comparisons += 1
            swaps += 1
            mas[i], mas[j] = mas[j], mas[i]

    def sort(low, high):
        if low < high:
            split_index = partition(low, high)
            sort(low, split_index)
            sort(split_index + 1, high)

    sort(0, len(mas) - 1)
    iterations = comparisons + swaps
    return iterations, comparisons, swaps


def generate_array(size, order):
    mas = list(range(1, size + 1))
    if order == 'Случайный':
        random.shuffle(mas)
    elif order == 'Сортированный':
        mas.sort()
    elif order == 'Обратный':
        mas.sort(reverse=True)
    elif order == '25%':
        n = int(size * 0.25)
        mas[:n].sort()
        random.shuffle(mas[n:])
    elif order == '50%':
        n = int(size * 0.5)
        mas[:n].sort()
        random.shuffle(mas[n:])
    elif order == '75%':
        n = int(size * 0.75)
        mas[:n].sort()
        random.shuffle(mas[n:])
    return mas


sizes = [20, 500, 1000, 3000, 5000, 10000]
orders = ['Случайный', 'Сортированный', 'Обратный', '25%', '50%', '75%']
results = {}

# Тестирование
for size in sizes:
    for order in orders:
        mas = generate_array(size, order)
        bubble_iterations, bubble_comparisons, bubble_exchanges = bubble_sort(mas.copy())
        selection_iterations, selection_comparisons, selection_exchanges = selection_sort(mas.copy())
        insertion_iterations, insertion_comparisons, insertion_exchanges = insertion_sort(mas.copy())
        quick_iterations, quick_comparisons, quick_swaps = quick_sort(mas.copy())

        results[(size, order)] = {
            'Bubble Sort': {'Time': timeit.timeit(lambda: bubble_sort(mas.copy()), number=1),
                            'Iterations': bubble_iterations,
                            'Comparisons': bubble_comparisons,
                            'Exchanges': bubble_exchanges},
            'Selection Sort': {'Time': timeit.timeit(lambda: selection_sort(mas.copy()), number=1),
                               'Iterations': selection_iterations,
                               'Comparisons': selection_comparisons,
                               'Exchanges': selection_exchanges},
            'Insertion Sort': {'Time': timeit.timeit(lambda: insertion_sort(mas.copy()), number=1),
                               'Iterations': insertion_iterations,
                               'Comparisons': insertion_comparisons,
                               'Exchanges': insertion_exchanges},
            'Quick Sort': {'Time': timeit.timeit(lambda: quick_sort(mas.copy()), number=1),
                           'Iterations': quick_iterations,
                           'Comparisons': quick_comparisons,
                           'Swaps': quick_swaps}
        }

# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

df = pd.DataFrame.from_dict(results, orient="index")

# Вывод DataFrame
print(df)
