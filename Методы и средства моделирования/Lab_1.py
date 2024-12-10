from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
from sympy import lambdify, symbols
import sympy as sp
from sympy import Function, Eq, symbols, sqrt, dsolve


def read_cauchy_problem():
    """
    Считывает ввод пользователя для задачи Коши.

    Возвращает:
        - функцию f(x, y) в виде lambda
        - начальное условие (x0, y0)
        - интервал решения (x_min, x_max).
    """
    print("Введите правую часть дифференциального уравнения в виде f(x, y). Например, 'x + y'.")
    f_input = input("f(x, y) = ")

    # Проверяем ввод на корректность и создаём функцию
    x, y = sp.symbols('x y')
    try:
        # Символическое преобразование строки в выражение
        f_expr = sp.sympify(f_input)

        # Проверяем, что выражение корректное и поддерживает sqrt, если нужно
        if isinstance(f_expr, sp.Basic) and 'sqrt' in str(f_expr):
            f_expr = sp.simplify(f_expr)  # Приводим к более простому виду

        # Создаём лямбда-функцию для числовых вычислений
        f_lambda = sp.lambdify((x, y), f_expr, 'numpy')

    except Exception as e:
        print(f"Ошибка при разборе уравнения: {e}")
        return None

    print("Введите начальное условие (x0, y0). Например, '0 1' для y(0) = 1.")
    try:
        x0, y0 = map(float, input("x0 y0 = ").split())
    except ValueError:
        print("Ошибка: начальные условия должны быть числами.")
        return None

    print("Введите интервал решения в виде двух чисел: x_min и x_max. Например, '0 5'.")
    try:
        x_min, x_max = map(float, input("x_min x_max = ").split())
        if x_min >= x_max:
            print("Ошибка: x_min должен быть меньше x_max.")
            return None
    except ValueError:
        print("Ошибка: границы интервала должны быть числами.")
        return None

    print("\nВвод завершён. Подробности задачи:")
    print(f"f(x, y) = {f_expr}")
    print(f"Начальное условие: x0 = {x0}, y0 = {y0}")
    print(f"Интервал решения: [{x_min}, {x_max}]")

    return f_lambda, (x0, y0), (x_min, x_max)


def solve_cauchy_explicit_euler(f, initial_conditions, interval, step_size):
    """
    Решает задачу Коши с использованием явной схемы Эйлера.

    Аргументы:
        - f: функция правой части f(x, y) (лямбда-выражение).
        - initial_conditions: кортеж (x0, y0), начальные условия.
        - interval: кортеж (x_min, x_max), интервал решения.
        - step_size: шаг интегрирования.

    Возвращает:
        - Списки x_values и y_values, содержащие точки решения.
    """
    x0, y0 = initial_conditions
    x_min, x_max = interval

    # Проверяем, что шаг корректен
    if step_size <= 0 or step_size > (x_max - x_min):
        raise ValueError("Шаг должен быть положительным и меньше длины интервала.")

    # Списки для хранения результатов
    x_values = [x0]
    y_values = [y0]

    # Выполняем шаги метода Эйлера
    x = x0
    y = y0
    while x < x_max:
        y = y + step_size * f(x, y)  # Схема Эйлера
        x = x + step_size
        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


def solve_cauchy_implicit_euler(f, initial_conditions, interval, step_size):
    """
    Решает задачу Коши с использованием неявной схемы Эйлера.

    Аргументы:
        - f: функция правой части f(x, y) (лямбда-выражение).
        - initial_conditions: кортеж (x0, y0), начальные условия.
        - interval: кортеж (x_min, x_max), интервал решения.
        - step_size: шаг интегрирования.

    Возвращает:
        - Списки x_values и y_values, содержащие точки решения.
    """
    x0, y0 = initial_conditions
    x_min, x_max = interval

    # Проверяем, что шаг корректен
    if step_size <= 0 or step_size > (x_max - x_min):
        raise ValueError("Шаг должен быть положительным и меньше длины интервала.")

    # Списки для хранения результатов
    x_values = [x0]
    y_values = [y0]

    # Выполняем шаги метода Эйлера
    x = x0
    y = y0
    while x < x_max:
        x_next = x + step_size

        # Определяем функцию для решения уравнения
        def implicit_eq(y_next):
            return y_next - y - step_size * f(x_next, y_next)

        # Решаем нелинейное уравнение для y_next
        y_next = fsolve(implicit_eq, y)[0]  # y текущего шага — начальное приближение
        x = x_next
        y = y_next

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


def solve_cauchy_weighted_scheme(f, initial_conditions, interval, step_size, theta):
    """
    Решает задачу Коши с использованием схемы с весами.

    Аргументы:
        - f: функция правой части f(x, y) (лямбда-выражение).
        - initial_conditions: кортеж (x0, y0), начальные условия.
        - interval: кортеж (x_min, x_max), интервал решения.
        - step_size: шаг интегрирования.
        - theta: весовая параметр схемы (0 <= theta <= 1).

    Возвращает:
        - Списки x_values и y_values, содержащие точки решения.
    """
    x0, y0 = initial_conditions
    x_min, x_max = interval

    # Проверяем корректность параметров
    if not (0 <= theta <= 1):
        raise ValueError("Параметр theta должен быть в диапазоне [0, 1].")
    if step_size <= 0 or step_size > (x_max - x_min):
        raise ValueError("Шаг должен быть положительным и меньше длины интервала.")

    # Списки для хранения результатов
    x_values = [x0]
    y_values = [y0]

    # Выполняем шаги метода
    x = x0
    y = y0
    while x < x_max:
        x_next = x + step_size

        # Определяем функцию для решения уравнения
        def weighted_eq(y_next):
            return y_next - y - step_size * (
                    theta * f(x_next, y_next) + (1 - theta) * f(x, y)
            )

        # Решаем нелинейное уравнение для y_next
        if theta == 0:  # Явная схема Эйлера (упрощённый случай)
            y_next = y + step_size * f(x, y)
        else:
            y_next = fsolve(weighted_eq, y)[0]  # Начальное приближение — y

        x = x_next
        y = y_next

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


def solve_cauchy_analytically(f_lambda, initial_conditions):
    """
    Решает задачу Коши аналитически, если возможно.

    Аргументы:
        - f_lambda: лямбда-функция, задающая правую часть f(x, y), например, lambda x, y: x + y.
        - initial_conditions: кортеж (x0, y0), начальные условия.

    Возвращает:
        - Символьное выражение решения или сообщение об отсутствии аналитического решения.
    """
    # Определяем символы
    x = symbols('x')
    y = Function('y')(x)

    # Задаём дифференциальное уравнение с правой частью, заданной лямбда-функцией
    try:
        f_expr = f_lambda(x, y)  # Получаем символьное выражение правой части уравнения
    except Exception as e:
        return f"Ошибка выполнения функции: {e}"

    # Задаём дифференциальное уравнение с использованием символьного выражения
    ode = Eq(y.diff(x), f_expr)

    # Применяем начальные условия
    x0, y0 = initial_conditions

    try:
        # Пытаемся решить уравнение аналитически
        solution = dsolve(ode, y, ics={y.subs(x, x0): y0})
        return solution
    except Exception as e:
        return f"Ошибка решения уравнения: {e}"


def plot_multiple_solutions(explicit_solution=None, implicit_solution=None, weighted_solution=None,
                            analytical_solution=None, interval=None, title="Решение задачи Коши"):
    """
    Строит график для трёх численных методов и аналитического решения задачи Коши.

    Аргументы:
        - explicit_solution: кортеж (x_values, y_values) для явной схемы Эйлера.
        - implicit_solution: кортеж (x_values, y_values) для неявной схемы Эйлера.
        - weighted_solution: кортеж (x_values, y_values) для схемы с весами.
        - analytical_solution: символьное выражение аналитического решения.
        - interval: кортеж (x_min, x_max) для построения аналитического решения.
        - title: заголовок графика (по умолчанию "Решение задачи Коши").
    """
    plt.figure(figsize=(12, 8))

    # Построение численных решений
    if explicit_solution:
        x_explicit, y_explicit = explicit_solution
        plt.plot(x_explicit, y_explicit, label="Явный метод Эйлера", color='blue')

    if implicit_solution:
        x_implicit, y_implicit = implicit_solution
        plt.plot(x_implicit, y_implicit, label="Неявный метод Эйлера", color='green')

    if weighted_solution:
        x_weighted, y_weighted = weighted_solution
        plt.plot(x_weighted, y_weighted, label="Метод с весами", color='purple')

    # Построение аналитического решения
    if analytical_solution is not None and interval:
        x_min, x_max = interval
        x_symbol = symbols('x')
        y_func = lambdify(x_symbol, analytical_solution.rhs, modules="numpy")  # Преобразуем в численную функцию
        x_vals = np.linspace(x_min, x_max, 500)
        y_vals = y_func(x_vals)
        plt.plot(x_vals, y_vals, label="Аналитическое решение", color='orange')

    # Настройка графика
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


# Пример использования
cauchy_data = read_cauchy_problem()
if cauchy_data:
    f_lambda, initial_conditions, interval = cauchy_data
    step_size = 0.1
    theta = 0.5

    # Численные решения
    explicit_solution = solve_cauchy_explicit_euler(
        f_lambda,  # Передаем f_lambda как функцию
        initial_conditions,
        interval,
        step_size
    )

    implicit_solution = solve_cauchy_implicit_euler(
        f_lambda,  # Передаем f_lambda как функцию
        initial_conditions,
        interval,
        step_size
    )

    weighted_solution = solve_cauchy_weighted_scheme(
        f_lambda,  # Передаем f_lambda как функцию
        initial_conditions,
        interval,
        step_size,
        theta
    )

    # Аналитическое решение
    analytical_solution = solve_cauchy_analytically(f_lambda, initial_conditions)

    # Построение графика
    plot_multiple_solutions(
        explicit_solution=explicit_solution,
        implicit_solution=implicit_solution,
        weighted_solution=weighted_solution,
        analytical_solution=analytical_solution,
        interval=interval,
        title="Сравнение численных методов и аналитического решения"
    )

