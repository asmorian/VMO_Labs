import tkinter as tk
from tkinter import ttk
import sys


def matrix_chain_order(p, i, j):
    if i == j:
        return 0

    _min = sys.maxsize
    for k in range(i, j):

        count = (matrix_chain_order(p, i, k)
                 + matrix_chain_order(p, k + 1, j)
                 + p[i - 1] * p[k] * p[j])

        if count < _min:
            _min = count

    return _min


def new_win(value):
    resp_win = tk.Tk()
    resp_win.title("Ответ")
    resp_win.geometry("200x50")
    resp_text = ttk.Label(resp_win, text="Ответ:")
    resp_text2 = ttk.Label(resp_win, text=value)
    resp_text.pack()
    resp_text2.pack()


def button_clicked():
    lst = dim_entry.get()
    lst = lst.split(",")
    lst = list(map(int, lst))
    size = len(lst)
    new_win(matrix_chain_order(lst, 1, size - 1))


# Окно
main_win = tk.Tk()
main_win.title("Задача об умножении матриц")
main_win.geometry("300x100")

dimension_label = ttk.Label(main_win, text="Введите список размерностей матриц")
dimension_label.pack()

dim_entry = ttk.Entry()
dim_entry.pack()

create_button = tk.Button(main_win, text="Рассчитать", command=button_clicked)
create_button.pack()

main_win.mainloop()
