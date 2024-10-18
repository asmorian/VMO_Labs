from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Определяем символы
x, y, lam = symbols("x y lam")


def extremes_func(u, f):
    # Функция Лагранжа
    L = u + lam * f

    # Частные производные функции L
    Lx = diff(L, x)
    Ly = diff(L, y)

    # Стационарные точки
    variables = solve([Lx, Ly, f], [x, y, lam])
    M = {x: variables[x], y: variables[y], lam: variables[lam]}

    # Вычисление определителя (дельта)
    Lxx = diff(Lx, x)
    Lyy = diff(Ly, y)
    Lxy = diff(Lx, y)
    fx, fy = diff(f, x), diff(f, y)
    delta = -(Matrix([[0, fx, fy], [fx, Lxx, Lxy], [fy, Lxy, Lyy]]).det())

    u_res = u.subs([(x, M[x]), (y, M[y])])

    # Итоговая проверка на наличие условного минимума/максимума в точке M
    if delta > 0:
        return f"Условный минимум {float(u_res)} в точке ({M[x]}, {M[y]})"
    elif delta < 0:
        return f"Условный максимум {float(u_res)} в точке ({M[x]}, {M[y]})"
    else:
        return "Нет условного экстремума"


# Построение итоговой поверхности
def plot_suface(px, py, equation, con):
    equation_lambda = lambdify((x, y), equation)
    con_lambda = lambdify((x, y), con)
    x_vals = np.linspace(-10, 10, 100)
    y_vals = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = equation_lambda(X, Y)
    Z1 = con_lambda(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='inferno_r', alpha=0.6)
    ax.plot_surface(X, Y, Z1, alpha=0.3)
    point_x = px
    point_y = py
    point_z = equation_lambda(point_x, point_y)
    ax.scatter(point_x, point_y, point_z, color='blue', s=100)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


# Функция для обработки нажатия кнопки
def on_calculate():
    try:
        t1 = entry_function.get()
        t2 = entry_condition.get()

        u = simplify(t1, evaluate=False)
        f = simplify(t2, evaluate=False)

        # Вычисление экстремума
        result = extremes_func(u, f)

        # Отображение результата
        text_area.delete(1.0, tk.END)  # Очищаем текстовое поле
        text_area.insert(tk.END, result)  # Вставляем новый результат

        # Проверка для построения поверхности
        if "минимум" in result or "максимум" in result:
            # Получаем координаты для графика
            variables = solve([diff(u + lam * f, x), diff(u + lam * f, y), f], [x, y, lam])
            px, py = float(variables[x]), float(variables[y])
            plot_suface(px, py, u, f)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Создание интерфейса
root = tk.Tk()
root.title("Индивидуальное задание 3")

# Ввод функции
label_function = tk.Label(root, text="Введите функцию u(x,y):")
label_function.pack()
entry_function = tk.Entry(root, width=50)
entry_function.pack()

# Ввод условия
label_condition = tk.Label(root, text="Введите условие g(x,y):")
label_condition.pack()
entry_condition = tk.Entry(root, width=50)
entry_condition.pack()

# Кнопка для вычисления
button_calculate = tk.Button(root, text="Рассчитать", command=on_calculate)
button_calculate.pack()

# Текстовое поле для отображения результатов
text_area = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
text_area.pack()

# Настройка фокуса на текстовом поле
text_area.bind("<Button-1>", lambda e: text_area.focus_set())

# Запуск главного цикла Tkinter
root.mainloop()


#   2*x**2 - 2*x*y + y**2 - 2*x + 3*y + 8
#   2*x - y + 3
