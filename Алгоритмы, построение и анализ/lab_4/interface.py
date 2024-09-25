import tkinter as tk
from tkinter import ttk
from knapsack import knapsack, Item, fractional_knapsack


# Создание окна ответов
def new_win(value, items):
    if items == 0:
        resp_win = tk.Tk()
        resp_win.title("Ответ")
        resp_win.geometry("200x50")
        resp_text = ttk.Label(resp_win, text="Ответ:")
        resp_text2 = ttk.Label(resp_win, text=value)
        resp_text.pack()
        resp_text2.pack()
    else:
        resp_win = tk.Tk()
        resp_win.title("Ответ")
        resp_win.geometry("200x100")
        resp_text = ttk.Label(resp_win, text="Ответ:")
        resp_text2 = ttk.Label(resp_win, text=value)
        resp_text.pack()
        resp_text2.pack()

        item_text = ttk.Label(resp_win, text="Входящие предметы:")
        item_text2 = ttk.Label(resp_win, text=items)
        item_text.pack()
        item_text2.pack()


# Окно ошибки
def error_win(error_name):
    err_win = tk.Tk()
    err_win.title("Ответ")
    err_win.geometry("200x50")
    err_text = ttk.Label(err_win, text="Ошибка:")
    err_text2 = ttk.Label(err_win, text=error_name)
    err_text.pack()
    err_text2.pack()


# Фун-ция кнопки
def button_clicked():
    if option_var.get() == "Дискретная":
        try:
            wt = wt_entry.get()
            wt = wt.split(",")
            wt = list(map(int, wt))
            val = val_entry.get()
            val = val.split(",")
            val = list(map(int, val))
            w = int(w_entry.get())
            length = int(n_entry.get())
            try:
                t = [[-1 for i in range(w + 1)] for j in range(length + 1)]
                v, it = knapsack(wt, val, w, length, t)
                new_win(v, it)
            except IndexError:
                error_win("Сравните кол-во элем-ов")

        except ValueError:
            error_win("Заполните поля!")

    elif option_var.get() == "Непрерывная":
        try:
            wt = wt_entry.get()
            wt = wt.split(",")
            wt = list(map(float, wt))
            val = val_entry.get()
            val = val.split(",")
            val = list(map(float, val))
            w = int(w_entry.get())
            length = int(n_entry.get())
            arr = []

            for i in range(int(length)):
                arr.append(Item(val[i], wt[i], i))

            v, it = fractional_knapsack(w, arr)
            new_win(v, it)

        except ValueError:
            error_win("Заполните поля!")


# Окно
main_win = tk.Tk()
main_win.title("Задача о рюкзаке")
main_win.geometry("300x300")

# Выбор задачи
options = ["Дискретная", "Непрерывная"]
option_var = tk.StringVar(value=options[0])
option_menu = ttk.Combobox(textvariable=option_var, values=options)
option_menu.pack(padx=6, pady=6)

# Ввод
w_label = ttk.Label(main_win, text="Максимальный вес")
w_entry = ttk.Entry()
w_label.pack()
w_entry.pack()

n_label = ttk.Label(main_win, text="Кол-во предметов")
n_entry = ttk.Entry()
n_label.pack()
n_entry.pack()

wt_label = ttk.Label(main_win, text="Введите веса (через запятую)")
wt_entry = ttk.Entry()
wt_label.pack()
wt_entry.pack()

val_label = ttk.Label(main_win, text="Введите стоимости (через запятую)")
val_entry = ttk.Entry()
val_label.pack()
val_entry.pack()
# Конец ввода


# Создание кнопки
sort_button = tk.Button(main_win, text="Сортировать", command=button_clicked)
sort_button.pack()

main_win.mainloop()
