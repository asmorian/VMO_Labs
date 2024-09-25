
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

