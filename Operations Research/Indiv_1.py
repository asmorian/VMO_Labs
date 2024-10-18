from PyQt5.QtWidgets import (QComboBox, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QScrollArea)
from PyQt5.QtCore import Qt
import sys
import sympy
from sympy import symbols, diff, lambdify
import numpy as np
import matplotlib.pyplot as plt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setWindowTitle("Индивидуальное задание 1")
        self.setGeometry(150, 300, 500, 100)

        # Создание элементов интерфейса
        self.lbl_el = QLabel("Функция: ")
        self.txtX0 = QLineEdit()
        self.start_btn = QPushButton("Вычислить")
        self.lbl_result = QLabel()

        # Размещение элементов в макетах
        self.init_layouts()

        # Подключение сигнала кнопки
        self.start_btn.clicked.connect(self.extr)

    def init_layouts(self):
        # Создание макетов
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        down_layout = QHBoxLayout()

        # Настройка верхнего макета
        top_layout.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.lbl_el)
        top_layout.addWidget(self.txtX0)
        top_layout.addWidget(self.start_btn)

        # Настройка нижнего макета
        down_layout.addWidget(self.lbl_result)

        # Добавление макетов в основной макет
        main_layout.addLayout(top_layout)
        main_layout.addLayout(down_layout)

        # Установка основного макета
        self.setLayout(main_layout)

    def extr(self):
        try:
            x, y = symbols('x y')
            z = self.txtX0.text().lower()
            z1 = sympy.sympify(z)
            f_func = lambdify([x, y], z1, 'numpy')

            # Вычисляем градиент функции
            grad_u = [diff(z, x), diff(z, y)]
            grad_u_2 = [diff(grad_u[0], x), diff(grad_u[0], y), diff(grad_u[1], y)]

            # Находим точки, в которых градиент равен нулю
            extrema_points = sympy.solve(grad_u, (x, y))

            # Если стационарных точек нет
            if not extrema_points:
                self.lbl_result.setText("Точки, в которых градиент равен 0, отсутствуют")
                return

            # Обработка каждой стационарной точки
            for i, point in enumerate(extrema_points):
                A = grad_u_2[0].subs(x, point[0])
                B = grad_u_2[1]
                C = grad_u_2[2].subs(y, point[1])

                # Проверка условия для экстремума
                if (A * C) - B ** 2 > 0:
                    point_val = z1.subs({x: point[0], y: point[1]})
                    extremum_type = "максимума" if point_val > 0 else "минимума"
                    self.lbl_result.setText(
                        f"M{i + 1} {point} точка {extremum_type}. \nЗначение точки: u(x,y) = {point_val}."
                    )
                    self.plot_surface(f_func, point, point_val)
                else:
                    self.lbl_result.setText(f"Точка M{i + 1} не имеет локальных экстремумов")
        except Exception:
            self.lbl_result.setText("Ошибка: проверьте ввод функции.")

    def plot_surface(self, f_func, point, point_val):
        # Построение графика поверхности
        X = np.linspace(-5, 5, 100)
        Y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(X, Y)
        Z = f_func(X, Y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, alpha=0.25)
        ax.scatter(point[0], point[1], point_val, color='b', s=25)
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# x**2 + 6*x + y**3 + 4*y**2 - 3*y + 5
