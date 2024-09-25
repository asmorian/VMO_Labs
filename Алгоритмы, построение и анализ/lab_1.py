import tkinter as tk
from tkinter import ttk
import random as rnd
import time as tm


# Вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# Выбором
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# Обменом (Пузырёк)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# Быстрая
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        q = rnd.choice(arr)
        s_arr = []
        b_arr = []
        e_arr = []
        for n in arr:
            if n < q:
                s_arr.append(n)
            elif n > q:
                b_arr.append(n)
            else:
                e_arr.append(n)
        return quick_sort(s_arr) + e_arr + quick_sort(b_arr)


# Бинарное дерево
class BinSearchTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def insert_elem(self, node):
        if self.key > node.key:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert_elem(node)
        elif self.key <= node.key:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert_elem(node)

    def inorder_traversal(self, sorted_list):
        if self.left is not None:
            self.left.inorder_traversal(sorted_list)
        sorted_list.append(self.key)
        if self.right is not None:
            self.right.inorder_traversal(sorted_list)


class BinSearchTree:
    def __init__(self):
        self.root = None

    def inorder_traversal(self):
        sorted_list = []
        if self.root is not None:
            self.root.inorder_traversal(sorted_list)
        return sorted_list

    def add_val(self, key):
        new_node = BinSearchTreeNode(key)
        if self.root is None:
            self.root = new_node
        else:
            self.root.insert_elem(new_node)


# Шелла
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# Пирамидальная
def building_tree(arr, tree_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    if left_child < tree_size and arr[left_child] > arr[largest]:
        largest = left_child
    if right_child < tree_size and arr[right_child] > arr[largest]:
        largest = right_child
    if largest != root_index:
        arr[root_index], arr[largest] = arr[largest], arr[root_index]
        building_tree(arr, tree_size, largest)


def pyramidal_sort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        building_tree(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        building_tree(arr, i, 0)
    return arr


# Слиянием
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


array = []


# Создание списка
def create_array(num):
    array.clear()
    for i in range(num.get()):
        array.append(rnd.randint(-100000, 100000))


# Окно вывода отсортированного списка
def sorted_win(sorted_array, method_name):
    result_win = tk.Tk()
    result_win.title(method_name)
    result_win.geometry("300x400")
    array_str = '\n'.join(map(str, sorted_array))
    text = tk.Text(result_win, wrap=tk.WORD)
    text.insert(tk.END, array_str)
    text.pack()


def error_win():
    err_win = tk.Tk()
    err_win.title("Ошибка ввода!")
    err_win.geometry("300x100")
    err_text = tk.Text(err_win)
    err_text.insert(tk.END, "Неверный формат ввода!\nПроверьте выбраны ли методы и верно ли введена длина массива")
    err_text.pack()


# Функция вызова сортировки
def sort_button_clicked():
    comparison_array = []
    create_array(option_var)

    if option_var.get() <= 0:
        error_win()

    else:
        if checkbox_var1.get() == 1:
            ins_first = tm.time()
            ins_sorted = insertion_sort(array)
            ins_second = tm.time()
            ins_time = ins_second - ins_first
            sorted_win(ins_sorted, "Вставками")
            comparison_array.append([ins_time, "Вставками"])

        if checkbox_var2.get() == 1:
            sel_first = tm.time()
            sel_sorted = selection_sort(array)
            sel_second = tm.time()
            sel_time = sel_second - sel_first
            sorted_win(sel_sorted, "Выбором")
            comparison_array.append([sel_time, "Выбором"])

        if checkbox_var3.get() == 1:
            bub_first = tm.time()
            bub_sorted = bubble_sort(array)
            bub_second = tm.time()
            bub_time = bub_second - bub_first
            sorted_win(bub_sorted, "Пузырьком")
            comparison_array.append([bub_time, "Пузырьком"])

        if checkbox_var4.get() == 1:
            quick_first = tm.time()
            quick_sorted = quick_sort(array)
            quick_second = tm.time()
            sorted_win(quick_sorted, "Быстрая")
            quick_time = quick_second - quick_first
            comparison_array.append([quick_time, "Быстрая"])

        if checkbox_var5.get() == 1:
            tree_first = tm.time()
            instance = BinSearchTree()
            for item in array:
                instance.add_val(item)
            tree_sorted = instance.inorder_traversal()
            tree_second = tm.time()
            tree_time = tree_second - tree_first
            sorted_win(tree_sorted, "Деревом")
            comparison_array.append([tree_time, "Деревом"])

        if checkbox_var6.get() == 1:
            pyr_first = tm.time()
            pyr_sorted = pyramidal_sort(array)
            pyr_second = tm.time()
            pyr_time = pyr_second - pyr_first
            sorted_win(pyr_sorted, "Пирамидальная")
            comparison_array.append([pyr_time, "Пирамидальная"])

        if checkbox_var7.get() == 1:
            shell_first = tm.time()
            shell_sorted = shell_sort(array)
            shell_second = tm.time()
            shell_time = shell_second - shell_first
            sorted_win(shell_sorted, "Шелла")
            comparison_array.append([shell_time, "Шелла"])

        if checkbox_var8.get() == 1:
            merge_first = tm.time()
            merge_sorted = merge_sort(array)
            merge_second = tm.time()
            merge_time = merge_second - merge_first
            sorted_win(merge_sorted, "Слиянием")
            comparison_array.append([merge_time, "Слиянием"])

        comparison_win = tk.Tk()
        comparison_win.title("Сравнение")
        comparison_array.sort()
        best_str = ' - '.join(map(str, comparison_array[0]))
        best = tk.Label(comparison_win, text=best_str)
        best.pack()
        mid_str = ' - '.join(map(str, comparison_array[len(comparison_array)//2]))
        mid = tk.Label(comparison_win, text=mid_str)
        mid.pack()
        worst_str = ' - '.join(map(str, comparison_array[len(comparison_array)-1]))
        worst = tk.Label(comparison_win, text=worst_str)
        worst.pack()


# Главное окно
main_win = tk.Tk()
main_win.title("Сортировка массивов")
main_win.geometry("300x300")

# Выбор размера массива
options = [5000, 10000, 100000, 150000, "Пользовательский"]
option_var = tk.IntVar(value=options[0])

option_menu = ttk.Combobox(textvariable=option_var, values=options)
option_menu.pack(padx=6, pady=6)


# Выбор метода сортировки
checkbox_var1 = tk.IntVar()
checkbox1 = ttk.Checkbutton(main_win, text="Сортировка вставками", variable=checkbox_var1)
checkbox1.pack()

checkbox_var2 = tk.IntVar()
checkbox2 = ttk.Checkbutton(main_win, text="Сортировка выбором", variable=checkbox_var2)
checkbox2.pack()

checkbox_var3 = tk.IntVar()
checkbox3 = ttk.Checkbutton(main_win, text="Сортировка обменом", variable=checkbox_var3)
checkbox3.pack()

checkbox_var4 = tk.IntVar()
checkbox4 = ttk.Checkbutton(main_win, text="Быстрая сортировка", variable=checkbox_var4)
checkbox4.pack()

checkbox_var5 = tk.IntVar()
checkbox5 = ttk.Checkbutton(main_win, text="Сортировка деревом", variable=checkbox_var5)
checkbox5.pack()

checkbox_var7 = tk.IntVar()
checkbox7 = ttk.Checkbutton(main_win, text="Сортировка Шелла", variable=checkbox_var7)
checkbox7.pack()

checkbox_var8 = tk.IntVar()
checkbox8 = ttk.Checkbutton(main_win, text="Сортировка слиянием", variable=checkbox_var8)
checkbox8.pack()

checkbox_var6 = tk.IntVar()
checkbox6 = ttk.Checkbutton(main_win, text="Пирамидальная сортировка", variable=checkbox_var6)
checkbox6.pack()


# Кнопка запуска
sort_button = tk.Button(main_win, text="Сортировать", command=sort_button_clicked)
sort_button.pack()

main_win.mainloop()
