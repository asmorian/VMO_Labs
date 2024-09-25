from Lab3_sort import insertion_sort, quick_sort, bubble_sort, selection_sort
import random
import timeit
import pandas as pd


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

for size in sizes:
    for order in orders:
        if size == 20:
            string = input("Введите числа через запятую: ")
            mas = string.split(",")
            print(mas)
            for nums in mas:
                int(nums)
        else:
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

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

df = pd.DataFrame.from_dict(results, orient="index")

print(df)

