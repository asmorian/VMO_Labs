from sympy import *
from sympy import symbols, Integral, Piecewise, Basic, Equality, Float, Expr, Add
from sympy.core.relational import Relational
from sympy.integrals import integrate
from sympy.integrals.risch import NonElementaryIntegral
from sympy.plotting import plot
from typing import Tuple, List, Any
import scipy.integrate as sc_integrate
import seaborn as sns
import numpy as np
import copy
import re


# Программная реализация решения интегральных уравнений Фредгольма и Вольтерра 2-го рода
# методами Симпсона и трапеций.
class IntegralEquation:
    def __init__(self, eq_type, method, lmd, a, b, n, ks, fx):
        # Базовые переменные
        self.y, self.x, self.s, self.xi, self.yi, self.ds, self.fi = symbols("y, x, s, xi, yi, ds, φ")
        # Тип уравнения (Фредгольма или Вольтерра)
        self.eq_type = eq_type
        # Метод решения (Симпсона или трапеций)
        self.method = method
        # Делитель шага в используемой формуле
        self.method_divisor = 6 if self.method == "Симпсона" else 4
        # Множитель слагаемого в используемой формуле
        self.method_mult = 4 if self.method == "Симпсона" else 2
        # Параметр интегрального ур-ия (лямбда)
        self.lmd = lmd
        # Нижний предел интегрирования
        self.a = a
        # Верхний предел интегрирования
        self.b = b
        # Количество отрезков деления
        self.n = n
        # Ядро интегрального ур-ия
        self.ks = ks
        # Известная функция
        self.fx = fx
        # Шаг деления на отрезки
        self.h = (self.b - self.a) / self.n
        # Количество итераций численного метода
        self.iters = self.get_num_of_iterations()
        # Переменные s0, s1, ..., sn
        self.s_col = symbols(" ".join(f"s{i}" for i in range(self.n + 1)), real=True)
        # Переменные y0, y1, ..., yn
        self.y_col = symbols(" ".join(f"y{i}" for i in range(self.n + 1)), real=True)

    # IntegralEquation.divide_intervals()
    # -----------------------------------
    # Делит интервал [a,b] на отрезки
    # для последующих итераций
    # -----------------------------------
    def divide_intervals(self) -> tuple[list[float | Any], list[float | Any]]:
        left = self.a
        right = self.b
        x_ints = [self.a]
        current_h = 0
        # промежуточные разбиения между [a,b]
        while right > left and current_h <= self.n - 2:
            x_ints.append(round(float(left + self.h * (current_h + 1)), 2))
            right = right - self.h
            current_h += 1
        x_ints.append(self.b)
        s_ints = copy.deepcopy(x_ints)
        return x_ints, s_ints

    # IntegralEquation.show_intervals()
    # --------------------------------
    # Выводит список интервалов по
    # переменным x и s в удобном
    # формате
    # --------------------------------
    def show_intervals(self) -> tuple[str, str]:
        x_ints, s_ints = self.divide_intervals()

        # Формируем строки
        x_i, y_i = 0, 0
        x_ints_str, s_ints_str = "", ""

        for cur_x, cur_s in zip(x_ints, s_ints):
            trail = ", " if x_i != len(x_ints) - 1 else ""
            x_ints_str += f"x{x_i} = {cur_x}{trail}"
            s_ints_str += f"s{x_i} = {cur_s}{trail}"
            x_i += 1
            y_i += 1

        return x_ints_str, s_ints_str

    # IntegralEquation.get_num_of_iterations()
    # --------------------------------
    # Возвращает количество итераций
    # численного метода
    # --------------------------------
    def get_num_of_iterations(self) -> int:
        x_ints, s_ints = self.divide_intervals()
        return len(x_ints)

    # IntegralEquation.general_form()
    # ------------------------------------
    # Генерация общего вида интегрального
    # уравнения второго рода
    # ------------------------------------
    def general_form(self) -> str:
        eq_core = "K*(x,s)" if self.eq_type == "Вольтерра" else "K(x,s)"
        upper_bound = "x" if self.eq_type == "Вольтерра" else "b"
        return f"y(x) - λ * ∫(a, {upper_bound}){eq_core}φ(s)ds = f(x)"

    # IntegralEquation.get_start_view()
    # ------------------------------------------------------------
    # Генерация частного вида интегрального уравнения.
    # ------------------------------------------------------------
    def get_start_view(self) -> str:
        lamb = abs(self.lmd) if self.lmd < 0 else self.lmd
        view = f"y(x) - {lamb} * "
        view += f"∫({self.a}, {self.b})"
        view += f"({self.ks})" if self.eq_type == "Фредгольма" else "K*(x,s)"
        view += f"y(s)ds = {self.fx}"
        return view

    # IntegralEquation.get_view_in_split_points()
    # --------------------------------------------------
    # Генерация общего вида интегрального уравнения
    # в точках деления.
    # -----------------------------------------------
    def get_view_in_split_points(self) -> str:
        if self.eq_type == "Фредгольма":
            return self.get_start_view() \
                .replace("f(x)", f"{self.fx}") \
                .replace("x", "xi") \
                .replace("λ", f"{self.lmd}") \
                .replace("(a, b)", f"({self.a}, {self.b})") + f", i = (0, {self.n})"
        elif self.eq_type == "Вольтерра":
            return self.general_form() \
                .replace("f(x)", f"{self.fx}") \
                .replace("x", "xi") \
                .replace("λ", f"{self.lmd}") \
                .replace("(a, b)", f"({self.a}, {self.b})") + f", i = (0, {self.n})"

    # IntegralEquation.get_integral_sum_common()
    # -----------------------------------------------
    # Генерация общего вида определенного интеграла
    # в виде интегральной суммы по методу
    # Симпсона/трапеций при заданном n
    # -----------------------------------------------
    def get_integral_sum_common(self) -> str:
        view_s = f"∫{self.a, self.b}φ(s)ds ≈ ((b - a) / {self.method_divisor}) * ["
        cur_int = 1

        # Заменяем k(s)φ(s) на представление в виде интегральной суммы по заданному методу.
        if self.method == "Симпсона":
            for i, cur_s in enumerate(self.s_col):
                if i == 0 or i == len(self.s_col) - 1:
                    view_s += f" + φ({cur_s})" if not view_s.endswith("[") else f"φ({cur_s})"
                elif i % 2 != 0:
                    view_s += f" + 4 * φ({cur_s})" if not view_s.endswith("[") else f"φ({cur_s})"
                    cur_int += 1
                else:
                    view_s += f" + 2 * φ({cur_s})" if not view_s.endswith("[") else f"4 * φ({cur_s})"
                    cur_int += 1
        elif self.method == "трапеций":
            for i, cur_s in enumerate(self.s_col):
                if i == 0 or i == len(self.s_col) - 1:
                    view_s += f" + φ({cur_s})" if not view_s.endswith("[") else f"φ({cur_s})"
                    cur_int += 1
                else:
                    view_s += f" + 2 * φ({cur_s})" if not view_s.endswith("[") else f"2 * φ({cur_s})"
                    cur_int += 1

        view_s += "]"

        return view_s

    # IntegralEquation.get_integral_sum_subs()
    # -----------------------------------------------
    # Генерация частного вида решения интегрального
    # уравнения с подставленными в интегральную
    # сумму частными значениями
    # -----------------------------------------------
    def get_integral_sum_subs(self) -> str:
        # Получаем разложение в виде конечной суммы
        raw = self.get_integral_sum_common()

        # Удаляем лишнюю информацию для парсинга библиотекой
        raw = raw.replace(f"∫{self.a, self.b}φ(s)ds ≈ ", "")

        # Заменяем (b - a) на разницу
        raw = raw.replace("(b - a)", str(self.b - self.a))

        # Добавляем после каждого φ(sn) в интегральной сумме соответствующий y0, y1, ..., yn
        for cur_s, cur_y in zip(self.s_col, self.y_col):
            raw = raw.replace(f"φ({cur_s})", f"φ({cur_s}) * {cur_y}")

        # Заменяем все φ(s1), φ(s2), ..., φ(sn) на соответствующий вид fx.
        for cur_s in self.s_col:
            raw = raw.replace(f"φ({str(cur_s)})", f"({self.ks.replace('x', 'xi').replace('s', str(cur_s))})")

        # Склеиваем все части, получая финальное разложение
        raw = f"yi - {self.lmd} * " + raw + f" = {self.fx}" + f", i = ({0}, {self.n})"

        return raw

    # IntegralEquation.generate_eq_sys()
    # ----------------------------------
    # Итерационное формирование системы
    # уравнений по заданному численному
    # методу
    # ----------------------------------
    def generate_eq_sys(self, round_coeff=False, decimals=2) -> dict[str | str]:
        expr = self.get_integral_sum_subs()
        # заменяем скобки
        prep_expr = expr.replace("[", "(").replace("]", ")")
        # удаляем правую часть уравнения
        prep_expr = prep_expr.replace(f" = {self.fx}", f"")
        # удаляем промежутки
        prep_expr = prep_expr.replace(f", i = (0, {self.n})", f"")
        # интервалы, таблица системы и текущая итерация
        x_ints, s_ints = self.divide_intervals()
        eqs = {}
        i = 0

        # Итерации численного метода
        for cur_y, cur_x in zip(self.y_col, x_ints):
            left_side = prep_expr
            # заменяем xi, yi на соответствующую переменную для i-го отрезка
            prep_cur_x = f"({cur_x})" if cur_x < 0 else cur_x
            left_side = left_side.replace(str(self.xi), str(prep_cur_x))
            left_side = left_side.replace(str(self.yi), str(cur_y))
            # на каждой итерации подставляем в cur_expr значения s0, s1,..., sn и вычисляем новую левую часть
            for cur_s, s_int in zip(self.s_col, s_ints):
                prep_cur_s = f"({s_int})" if s_int < 0 else s_int
                left_side = str(left_side).replace(str(cur_s), str(prep_cur_s))
            # если Вольтерра, то обнуляем коэффициенты "лесенкой"
            if self.eq_type == "Вольтерра":
                coeffs = list(Poly(parse_expr(left_side)).coeffs())
                j = i + 1
                # зануляем коэффы
                while j < len(coeffs):
                    coeffs[j] = 0
                    j += 1
                left_side = ""
                # заполняем ненулевые
                for y, coef in zip(self.y_col, coeffs):
                    coef = f"{coef}" if coef < 0 else f" + {coef}"
                    left_side += f"{coef}*{y}"
            # парсим выражение
            left_side = parse_expr(left_side)
            # если есть отрицательные коэфф-ы в левой части, помечаем флагом для дальнейшего инвертирования
            inverse = False
            if len(re.findall(r'(?<=- )?-(\d+)', str(left_side))) > 0:
                inverse = True
            # вычисляем правую часть уравнения
            right_side = parse_expr(str(f"{self.fx}").replace(str(self.x), str(cur_x)))
            # инвертируем обе части уравнения при необходимости
            if inverse:
                left_side *= -1
                right_side *= -1
            # если задан параметр, округляем коэффы
            if round_coeff:
                left_side = self.round_expr(left_side, decimals)
                right_side = self.round_expr(right_side, decimals)
            # записываем готовое уравнение системы
            eqs[f"i = {i}"] = str(left_side) + " = " + str(right_side)
            i += 1

        # Полученный словарь системы
        return eqs

    # IntegralEquation.get_sys_coeffs()
    # ---------------------------------
    # Вычленение матрицы коэффициентов
    # и вектора решений из системы
    # уравнений
    # ---------------------------------
    def get_sys_coeffs(self, decimals=2) -> tuple[list[list[float]], list[float]]:
        eqs = self.generate_eq_sys()
        matrix, vector = [], []

        # Вычленяем коэффициенты из каждого уравнения.
        for i, eq in eqs.items():
            eq_arr = eq.split(" = ")

            # Добавляем коэффициенты левой части в матрицу коэффициентов.
            left_side = eq_arr[0]
            expr_coeffs_dict = dict(parse_expr(left_side).as_coefficients_dict())
            coeffs_dict = {str(cur_y): 0 for cur_y in self.y_col}
            for cur_y, coef in expr_coeffs_dict.items():
                coeffs_dict[str(cur_y)] = round(float(coef), decimals)
            matrix.append(list(coeffs_dict.values()))

            # Добавляем правую часть в вектор.
            right_side = float(eq_arr[1])
            vector.append(right_side)

        # Готовые матрица коэффициентов и вектор свободных членов.
        return matrix, vector

    # IntegralEquation.get_sys_roots()
    # ---------------------------------
    # Возвращает вектор решения системы
    # уравнений по данным коэффициентам
    # (используется метод Гаусса)
    # ---------------------------------
    # АРГУМЕНТЫ:
    # --decimals = количество знаков
    # после запятой в каждом корне
    # ---------------------------------
    def get_sys_roots(self, decimals=4) -> list:
        m, vect = self.get_sys_coeffs()
        return [round(r, decimals) for r in list(self.gaussian(np.array(m), np.array(vect)))]

    # IntegralEquation.get_analityc_view()
    # ------------------------------------
    # Формирует аналитическое выражение
    # ------------------------------------
    def get_analityc_view(self) -> str:
        # -------------
        # БАЗОВАЯ ЧАСТЬ
        # -------------
        final_view = f"y(x) ≈ {self.fx} + {float(self.lmd * ((self.b - self.a) / self.method_divisor))}["
        # ----------------------------
        # ОСНОВНАЯ ИТЕРАЦИОННАЯ ЧАСТЬ
        # ----------------------------
        expr = self.get_integral_sum_subs()
        expr = expr[expr.find("["):]
        prep_expr = expr.replace("[", "").replace("]", "")
        # удаляем правую часть уравнения
        prep_expr = prep_expr.replace(f" = {self.fx}", f"")
        # удаляем промежутки
        prep_expr = prep_expr.replace(f", i = (0, {self.n})", f"")
        # интервалы и переменная для записи
        x_ints, s_ints = self.divide_intervals()
        central_part = ""

        # Запись интеграла в виде интегральной (конечной) суммы.
        for _ in zip(self.y_col):
            central_part = prep_expr
            # заменяем все xi на x
            central_part = central_part.replace(str(self.xi), str(self.x))
            # на каждой итерации подставляем в cur_expr значения s0, s1,..., sn
            for cur_s, s_int in zip(self.s_col, s_ints):
                prep_s_int = f"({s_int})" if s_int < 0 else s_int
                central_part = str(central_part).replace(str(cur_s), str(prep_s_int))
            # удаляем десятичную часть у коэффициентов
            central_part = central_part.replace(".0", "")

        # Добавляем готовую запись интегральной суммы.
        final_view += str(self.round_expr(parse_expr(central_part, evaluate=False), 4)) + "]"

        # Необходимые данные для формирования вычисленной части
        subbed_view = final_view[final_view.find("≈") + 2:].replace("[", "*(").replace("]", ")")
        sys_coeffs = self.get_sys_roots()

        # Подставляем переменные y0, y1, ..., yn
        for cur_y, coef in zip(self.y_col, sys_coeffs):
            subbed_view = str(subbed_view).replace(str(cur_y), str(coef))

        # Запись решения с подставленными y0, y1, ..., yn
        subbed_view_hard = str(parse_expr(subbed_view, evaluate=False))

        # Вычисляем выражение с подставленными значениями c округленными
        # коэффициентами до 4 знака
        subbed_view = str(self.round_expr(parse_expr(str(subbed_view)), 4))

        # Добавляем в финальное решение
        final_view += " = " + subbed_view_hard + " = " + subbed_view

        # Полное аналитическое решение интегрального уравнения
        return final_view

    # IntegralEquation.compare_concise_with_analytic()
    # ------------------------------------------------
    # Осуществляет различные проверки вычислений,
    # в частности основной погрешности
    # ------------------------------------------------
    def compare_concise_with_analytic(self) -> tuple[str, Expr, list[float], list[float], float]:
        # Аналитическое выражение y(x)
        analytic = str(self.get_analityc_view().split(" = ")[2])

        # Подставляем в интегральное выражение K(x,s) и y(s)
        ys = parse_expr(analytic).subs(self.x, self.s)
        integral_sub = f"∫({self.ks}) * ({str(ys)})ds"

        # Получаем функцию ошибки g(x)
        integral_sub = integral_sub.replace("∫", "").replace("ds", "")
        integrated = ""
        if self.eq_type == "Фредгольма":
            integrated = integrate(integral_sub, (self.s, self.a, self.b))
        elif self.eq_type == "Вольтерра":
            integrated = integrate(integral_sub, (self.s, self.a, self.x))
        gx = self.lmd * integrated + parse_expr(self.fx)
        gx = self.round_expr(gx, num_digits=4)

        # Находим игреки f(x) и g(x) на интервале [start, end] по иксу
        start, end = self.a - 10, self.b + 10
        yx_arr, gx_arr = [], []
        for cur_x in range(start, end + 1):
            yx_arr.append(round(float(parse_expr(analytic).subs(self.x, cur_x)), 4))
            gx_arr.append(round(float(gx.subs(self.x, cur_x)), 4))

        # Находим максимум по модулю (погрешность)
        error = round(max([abs(y_yx - y_gx) for y_yx, y_gx in zip(yx_arr, gx_arr)]), 4)

        # Возвращаем результаты
        return analytic, gx, yx_arr, gx_arr, error

    # IntegralEquation.visualize()
    # ------------------------------------------
    # Строит график вычисленного аналитического
    # решения - кривой функции y(x)
    # ------------------------------------------
    def visualize(self) -> None:
        # Вывод информации о погрешности
        self.get_check_result_in_console()
        # Функции для вывода на графике
        a_view = self.get_analityc_view()
        yx = parse_expr(a_view.split(" = ")[2])
        gx = self.compare_concise_with_analytic()[1]
        # Настройка сетки в выводимом графике
        sns.set()
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        # Формирование графика
        yx_plot = plot(yx,
                       title=f"Визуализация аналитического решения y(x) = {yx}",
                       show=False,
                       legend=True,
                       xlim=(-5, 5),
                       ylim=(-5, 5))
        gx_plot = plot(gx,
                       show=False,
                       legend=True,
                       xlim=(-5, 5),
                       ylim=(-5, 5))
        yx_plot.extend(gx_plot)
        # Отображение графика
        yx_plot.show()

    # IntegralEquation.gaussian()
    # ------------------------------------------------------
    # Статический метод
    # Решает матричное умножение A * b = x по
    # методу Гаусса.
    # ------------------------------------------------------
    # Принимает на вход две переменные:
    # A - матрица коэффициентов - квадратный двумерный
    # numpy array типа float
    # b - вектор свободных членов - numpy array типа float
    # Вовращает вектор решений
    # -------------------------------------------------------
    @staticmethod
    def gaussian(A, b) -> np.array:
        # составляем расширенную матрицу системы
        reshaped_b = b.reshape((len(b), 1))
        A = np.hstack((A, reshaped_b))

        # приводим матрицу к треугольному виду
        # i - опорная строка
        # j - текущая строка (всегда меньше i)
        for i in range(len(A)):
            for j in range(i + 1, len(A)):
                A[j] -= A[i] * A[j][i] / A[i][i]

        # обратный ход
        x = np.array([0] * len(b), dtype=float)  # вектор решений

        i = len(A) - 1
        while i >= 0:
            x[i] = (A[i][-1] - sum(x * A[i][0:-1])) / A[i][i]
            i -= 1

        # вектор решений
        return x

    # IntegralEquation.round_expr()
    # ---------------------------------------
    # Статический метод
    # Возвращает Sympy-выражение с коэфф-ами,
    # округленными до num_digits
    # ------------------------------------
    # АРГУМЕНТЫ
    # --dic = словарь для вывода
    # --delimiter = разделитель между
    # ключом и значением
    # --message = вывод сообщения
    # над выводом словаря
    # ---------------------------------------
    @staticmethod
    def round_expr(expr, num_digits) -> Expr:
        return expr.xreplace({n: round(float(n), num_digits) for n in expr.atoms(Number)})

    # IntegralEquation.round_matrix_coeffs()
    # ---------------------------------------
    # Статический метод
    # Возвращает матрица с коэфф-ами,
    # округленными до num_digits
    # ---------------------------------------
    # АРГУМЕНТЫ
    # --dic = словарь для вывода
    # --delimiter = разделитель между
    # ключом и значением
    # --message = вывод сообщения
    # над выводом словаря
    # ---------------------------------------
    @staticmethod
    def round_matrix_coeffs(matrix, decimals) -> list:
        return [[round(coef, decimals) for coef in eq] for eq in matrix]

    # IntegralEquation.pretty_dict_print()
    # ------------------------------------
    # Статический метод.
    # Вывод/возврат словаря в удобном виде
    # ------------------------------------
    # АРГУМЕНТЫ
    # --dic = словарь для вывода
    # --delimiter = разделитель между
    # ключом и значением
    # --message = вывод сообщения
    # над выводом словаря
    # ------------------------------------
    @staticmethod
    def pretty_dict_print(dic, delimiter=" => ", message="", ret=False) -> str | None:
        if message:
            print(message)
        if not ret:
            for key, value in dic.items():
                print(f"{key}{delimiter}", value)
            return
        final_str = ""
        for key, value in dic.items():
            final_str += f"{key}{delimiter}{value}\n"
        return final_str

    # IntegralEquation.pretty_matrix_print()
    # --------------------------------------
    # Статический метод.
    # Вывод матрицы в удобном виде
    # --------------------------------------
    # АРГУМЕНТЫ
    # --matrix = матрица для вывода
    # --message = вывод сообщения
    # над выводом словаря
    # --------------------------------------
    @staticmethod
    def pretty_matrix_print(matrix, message="", ret=False) -> str | None:
        if message:
            print(message)
        cop = copy.deepcopy(matrix)
        if not ret:
            for s in cop:
                print(s)
            return
        final_str = ""
        for s in cop:
            final_str += f"{s}\n"
        return final_str

    # IntegralEquation.get_check_result_console()
    # --------------------------------------------
    # Консольный вывод результатов проверки
    # погрешности вычислений
    # --------------------------------------------
    def get_check_result_in_console(self):
        yx, gx, y_yx, g_gx, error = self.compare_concise_with_analytic()
        print("Проверка (аналитическое выражение y(x))\n", yx)
        print("-" * 200)
        print("Проверка (функция ошибки g(x))\n", gx)
        print("-" * 200)
        print("Проверка (игреки y(x))\n", y_yx)
        print("-" * 200)
        print("Проверка (игреки g(x))\n", g_gx)
        print("-" * 200)
        print("Проверка (максимум по модулю разниц игреков f(x) и g(x) на интервале [a,b], она же погрешность)\n",
              error)
        print("-" * 200)

    # IntegralEquation.get_results()
    # -----------------------------------------
    # Консольный вывод вычисленных результатов
    # -----------------------------------------
    def get_console_results(self) -> None:
        matrix, vect = self.get_sys_coeffs()
        x_ints, s_ints = self.show_intervals()
        print("-" * 200)
        print("Интервалы по x\n", x_ints)
        print("Интервалы по S\n", s_ints)
        print(f"Общий вид интегрального уравнения {self.eq_type} 2-го рода\n", self.general_form())
        print("Частный вид интегрального уравнения\n", self.get_start_view())
        print("Частный вид интегрального уравнения в точках деления\n", self.get_view_in_split_points())
        print(f"Общий вид определенного интеграла в виде интегральной суммы по методу {self.method} при n = {self.n}\n",
              self.get_integral_sum_common())
        print("Частный вид решения интегрального уравнения с подставленными в интегральную сумму частными значениями\n",
              self.get_integral_sum_subs())
        print("-" * 200)
        self.pretty_dict_print(self.generate_eq_sys(round_coeff=True, decimals=2), " =>",
                               "Преобразованная система уравнений")
        print("-" * 200)
        self.pretty_matrix_print(matrix, "Матрица коэффициентов системы уравнений")
        print("-" * 200)
        print("Вектор свободных членов системы уравнений\n", vect)
        print("-" * 200)
        print("Корни системы уравнений\n", self.get_sys_roots())
        print("-" * 200)
        print("Финальное аналитическое решение\n", self.get_analityc_view())
        print("-" * 200)


# Меню работы с программой.
if __name__ == "__main__":
    eq_type = input("Введите тип интегрального уравнения (Фредгольма или Вольтерра) -> ")
    method = input("Введите используемый метод (трапеций или Симпсона) -> ")
    lmd = int(input("Введите параметр инт. уравнения (лямбда, λ) -> "))
    a = int(input("Введите нижний предел интегрирования a -> "))
    b = int(input("Введите верхний предел интегрирования b -> "))
    n = int(input("Введите кол-во разбиений отрезка интегрирования n -> "))
    ks = input("Введите ядро уравнения K(S) -> ")
    fx = input("Введите заданную функцию f(x) -> ")
    inst = IntegralEquation(eq_type, method, lmd, a, b, n, ks, fx)
    inst.get_console_results()
    inst.get_check_result_in_console()
    inst.visualize()
