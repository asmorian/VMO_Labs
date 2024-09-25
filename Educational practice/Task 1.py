from sympy import *
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.backends.backend_tkagg as tkagg
import numpy as np

# Задание символов
x, y, z = symbols('x y z')


# Первая производная
def der_1(formula):
    return diff(formula, x)


# Вторая производная
def der_2(formula):
    return diff(diff(formula, x))


# Метод хорд
def chord_method(formula, a, b, eps, nmax):
    iteration_array = [[], [], []]
    if formula.subs(x, a) * formula.subs(x, b) > 0:
        print("Корней нет")
        return iteration_array

    n = 1
    x_intermediate = a - (formula.subs(x, a)) / (formula.subs(x, b) - formula.subs(x, a)) * (b - a)
    iteration_array[0].append(n)
    iteration_array[1].append(x_intermediate)
    iteration_array[2].append(formula.subs(x, x_intermediate))

    while abs(formula.subs(x, x_intermediate)) > eps:
        n += 1
        if n > nmax:
            print("Превышено количество итераций, программа прервана")
            return iteration_array

        if formula.subs(x, x_intermediate) != 0:
            if formula.subs(x, a) * formula.subs(x, x_intermediate) < 0:
                b = x_intermediate
            else:
                a = x_intermediate

            x_intermediate = a - (formula.subs(x, a) / (formula.subs(x, b) - formula.subs(x, a))) * (b - a)
            iteration_array[0].append(n)
            iteration_array[1].append(x_intermediate)
            iteration_array[2].append(formula.subs(x, x_intermediate))
        else:
            return iteration_array


# Метод половинного деления
def method_of_half_division(formula, a, b, eps, nmax):
    iteration_array = [[], [], []]
    if formula.subs(x, a) * formula.subs(x, b) > 0:
        return print("Корней нет")
    else:
        n = 0
        while True:
            if abs(b-a) > eps:
                n += 1
                if n > nmax:
                    print("Превышено количество итераций, программа прервана")
                    return iteration_array
                x_intermediate = (a + b) / 2
                if formula.subs(x, x_intermediate) != 0:
                    if formula.subs(x, a) * formula.subs(x, x_intermediate) < 0:
                        b = x_intermediate
                    else:
                        a = x_intermediate
                    iteration_array[0].append(n)
                    iteration_array[1].append(x_intermediate)
                    iteration_array[2].append(formula.subs(x, x_intermediate))
                else:
                    return iteration_array
            else:
                return iteration_array


# Метод касательных
def tangent_method(formula, a, b, eps, nmax):
    iteration_array = [[], [], []]
    if formula.subs(x, a) * formula.subs(x, b) > 0:
        return print("Корней нет")
    else:
        if formula.subs(x, a) * der_2(formula).subs(x, a) > 0:
            x_intermediate = a
        else:
            x_intermediate = b
        n = 0
        h = 2 * eps
        while True:
            if abs(h) > eps:
                n += 1
                if n > nmax:
                    print("Превышено количество итераций, программа прервана")
                    return iteration_array
                h = - (formula.subs(x, x_intermediate) / der_1(formula).subs(x, x_intermediate))
                x_intermediate += h
                iteration_array[0].append(n)
                iteration_array[1].append(x_intermediate)
                iteration_array[2].append(formula.subs(x, x_intermediate))
            else:
                return iteration_array


# Окно ошибки
def error_win(name):
    err_win = Tk()
    err_win.title(name)
    err_win.geometry("250x200")
    err_label = Label(err_win, text="Корней нет", font="Courier 14")
    err_label.grid(row=0, column=0)


# Создание окна с таблицей решений
def win(result_array, name):
    result_win = Tk()
    result_win.title(name)
    result_win.geometry("600x400")

    columns = ("iter", "x", "f_x")

    tree = ttk.Treeview(result_win, columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)

    tree.heading("iter", text="Итерация")
    tree.heading("x", text="X")
    tree.heading("f_x", text="F(X)")

    res_array = []

    for i in range(len(result_array[0])):
        inter_array = [result_array[0][i], "{:.17f}".format(result_array[1][i]), "{:.17f}".format(result_array[2][i])]
        res_array.append(inter_array)

    for iteration in res_array:
        tree.insert("", END, values=iteration)


# Окно ошибки ввода
def void_win():
    void_wins = Tk()
    void_wins.title("Упс! Кажется произошла ошибка")
    void_wins.geometry("240x100")
    void_label = Label(void_wins, text="Заполните все поля!", font="Courier 14")
    void_label.grid(row=0, column=0)


# Функция вызываемая при нажатии кнопки "Начертить"
def graph():
    try:
        x_lpos = int(x_left_entry.get())
        x_rpos = int(x_right_entry.get())
        y_dpos = int(y_down_entry.get())
        y_upos = int(y_up_entry.get())
    except ValueError:
        x_lpos = -10
        x_rpos = 10
        y_dpos = -10
        y_upos = 10
    formula_string = formula_entry.get()
    try:
        formula = sympify(formula_string)
    except ValueError:
        void_win()
    plt.clf()
    x_vals = np.linspace(-10, 10, 1000)
    f = lambdify(x, formula, modules=['numpy'])
    f_vals = f(x_vals)
    plt.plot(x_vals, f_vals)
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_xlim(x_lpos, x_rpos)
    ax.set_ylim(y_dpos, y_upos)
    canvas.draw()


# Функция, вызываемая при нажатии кнопки "Рассчитать"
def calculate():
    formula_string = formula_entry.get()
    try:
        formula = sympify(formula_string)
        a = float(a_entry.get())
        b = float(b_entry.get())
        eps = float(eps_entry.get())
        nmax = int(nmax_entry.get())
    except ValueError:
        void_win()
    results = []

    # Функции привязанные к флажкам
    if chord_var.get() == 1:
        try:
            iterations, x_values, f_values = chord_method(formula, a, b, eps, nmax)
            results.append((iterations, x_values, f_values))
            win(chord_method(formula, a, b, eps, nmax), "Метод хорд")
        except TypeError:
            error_win("Метод хорд")

    if tangent_var.get() == 1:
        try:
            iterations, x_values, f_values = tangent_method(formula, a, b, eps, nmax)
            results.append((iterations, x_values, f_values))
            win(tangent_method(formula, a, b, eps, nmax), "Метод касательных")
        except TypeError:
            error_win("Метод касательных")

    if bisection_var.get() == 1:
        try:
            iterations, x_values, f_values = method_of_half_division(formula, a, b, eps, nmax)
            results.append((iterations, x_values, f_values))
            win(method_of_half_division(formula, a, b, eps, nmax), "Метод половинного деления")
        except TypeError:
            error_win("Метод половинного деления")

    graph()
    canvas.draw()


# Создание основного окна
window = Tk()
window.title("Численные методы решения нелинейных уравнений")
window.geometry("1440x600")

# Создание полей ввода и надписей
formula_label = Label(window, text="Формула f(x):", font="Courier 15")
formula_label.grid(row=0, column=0, sticky="w")
formula_entry = Entry(window)
formula_entry.grid(row=0, column=1)

a_label = Label(window, text="Начальная точка интервала a:", font="Courier 12")
a_label.grid(row=1, column=0, sticky="w")
a_entry = Entry(window)
a_entry.grid(row=1, column=1)

b_label = Label(window, text="Конечная точка интервала b:", font="Courier 12")
b_label.grid(row=2, column=0, sticky="w")
b_entry = Entry(window)
b_entry.grid(row=2, column=1)

eps_label = Label(window, text="Требуемая точность Eps:", font="Courier 12")
eps_label.grid(row=3, column=0, sticky="w")
eps_entry = Entry(window)
eps_entry.grid(row=3, column=1)

nmax_label = Label(window, text="Максимальное количество итераций:", font="Courier 12")
nmax_label.grid(row=4, column=0, sticky="w")
nmax_entry = Entry(window)
nmax_entry.grid(row=4, column=1)

x_left_label = Label(window, text="x1:")
x_left_entry = Entry(window, width=2)
x_right_label = Label(window, text="x2:")
x_right_entry = Entry(window, width=2)
y_down_label = Label(window, text="y1:")
y_down_entry = Entry(window, width=2)
y_up_label = Label(window, text="y2:")
y_up_entry = Entry(window, width=2)
x_left_entry.grid(row=5, column=5)
x_right_entry.grid(row=5, column=7)
y_down_entry.grid(row=5, column=9)
y_up_entry.grid(row=5, column=11)
x_left_label.grid(row=5, column=4)
x_right_label.grid(row=5, column=6)
y_down_label.grid(row=5, column=8)
y_up_label.grid(row=5, column=10)


# Создание флажков для выбора метода
method_frame = Frame(window)
method_frame.grid(row=0, column=2, rowspan=5, padx=10)

chord_var = IntVar()
chord_checkbutton = Checkbutton(method_frame, text="Метод хорд", variable=chord_var, font="Courier 12")
chord_checkbutton.pack(anchor="w")

tangent_var = IntVar()
tangent_checkbutton = Checkbutton(method_frame, text="Метод касательных", variable=tangent_var, font="Courier 12")
tangent_checkbutton.pack(anchor="w")

bisection_var = IntVar()
bisection_checkbutton = Checkbutton(method_frame, text="Метод половинного деления",
                                    variable=bisection_var, font="Courier 12")
bisection_checkbutton.pack(anchor="w")

# Создание кнопки "Рассчитать"
calculate_button = Button(window, text="Рассчитать", command=calculate)
calculate_button.grid(row=5, column=0, pady=5)

# Создание кнопки "Начертить"
graph_button = Button(window, text="Начертить", command=graph)
graph_button.grid(row=0, column=2, pady=1)

# Создание окна для графика
plot_frame = Frame(window)
plot_frame.grid(row=0, column=3, rowspan=6, padx=10, pady=10)
fig = plt.figure(figsize=(5, 5), dpi=100)
canvas = tkagg.FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()
plt.gca().set_aspect('equal', adjustable='box')

window.mainloop()
