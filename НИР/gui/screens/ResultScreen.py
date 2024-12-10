from gui.screens.ProgramScreen import *
from gui.custom.ColoredButton import *

import tkinter
from tkinter import font


# Экран с результатами вычислений и графиком.
class ResultScreen(ProgramScreen):
    def __init__(self, parent, controller, obj):
        ProgramScreen.__init__(self, parent, controller, self)

        # Размеры окна
        self.w_width = self.controller.width
        self.w_height = self.controller.height
        self.controller.set_geometry(self.w_width + 200, self.w_height + 80)

        # Объект класса, решающего интегральные уравнения
        self.obj = obj

        # Кнопка возврата на предыдущий экран программы
        self.canvas = Canvas(self, width=32, height=32, cursor="hand2")
        self.canvas.place(anchor=CENTER, relx=0.07, rely=0.07)
        self.backup_img = PhotoImage(file="images/backup-arrow.png")
        self.canvas.create_image(0, 0, anchor=NW, image=self.backup_img)
        self.canvas.bind("<Button-1>", self.controller.back_to_settings)

        # Заголовок текущего режима работы с программой.
        self.mode_label = Label(self,
                                text="Результат вычислений",
                                font=("Arial Bold", 12))
        self.mode_label.place(relx=0.5, rely=0.14, anchor=CENTER)

        # Оформление шрифтов.
        titles_font = font.Font(family="Arial", weight="bold", size=11)
        math_font = font.Font(family="Cambria", size=12)
        self.intervals_label = Label(self,
                                     text=f"Интервалы по x и S",
                                     font=titles_font,
                                     justify=LEFT)
        self.intervals_label.place(relx=0.05, rely=0.25, anchor=W)
        self.intervals_value = Label(self,
                                     text=f"{self.obj.divide_intervals()[0]}",
                                     font=math_font,
                                     justify=LEFT)
        self.intervals_value.place(relx=0.05, rely=0.29, anchor=W)

        self.common_eq_view_label = Label(self,
                                          text=f"Общий вид интегрального"
                                               f"\nуравнения {self.obj.eq_type} 2-го рода",
                                          font=titles_font,
                                          justify=LEFT)
        self.common_eq_view_label.place(relx=0.05, rely=0.36, anchor=W)
        self.common_eq_view_value = Label(self,
                                          text=f"{self.obj.get_common_view()}",
                                          font=math_font,
                                          justify=LEFT)
        self.common_eq_view_value.place(relx=0.05, rely=0.41, anchor=W)
        self.values_view_label = Label(self,
                                       text="Частный вид интегрального уравнения",
                                       font=titles_font,
                                       justify=LEFT)
        self.values_view_label.place(relx=0.05, rely=0.47, anchor=W)
        self.values_view_value = Label(self,
                                       text=f"{self.obj.get_start_view()}",
                                       font=math_font,
                                       justify=LEFT)
        self.values_view_value.place(relx=0.05, rely=0.51, anchor=W)

        self.common_integral_view_label = Label(self,
                                                text=f"Общий вид определенного интеграла в виде"
                                                     f"\nинтегральной суммы по методу {self.obj.method} при n = 2",
                                                font=titles_font,
                                                justify=LEFT)
        self.common_integral_view_label.place(relx=0.05, rely=0.58, anchor=W)
        self.common_integral_view_value = Label(self,
                                                text=f"{self.obj.get_integral_sum_common()}",
                                                font=math_font,
                                                justify=LEFT)
        self.common_integral_view_value.place(relx=0.05, rely=0.64, anchor=W)
        self.integral_sum_values_label = Label(self,
                                               text="Частный вид решения интегрального уравнения\n"
                                                    "с подставленными в интегральную сумму\n"
                                                    "частными значениями",
                                               font=titles_font,
                                               justify=LEFT)
        self.integral_sum_values_label.place(relx=0.05, rely=0.71, anchor=W)
        self.integral_sum_values_value = Label(self,
                                               text=f"{self.obj.get_integral_sum_subs()}",
                                               font=math_font,
                                               anchor=W,
                                               justify=LEFT)
        self.integral_sum_values_value.place(relx=0.05, rely=0.79, anchor=W)
        sys = self.obj.generate_eq_sys(round_coeff=True, decimals=2)
        delim = " => "
        self.eq_sys_label = Label(self,
                                  text="Преобразованная система уравнений",
                                  font=titles_font,
                                  justify=LEFT)
        self.eq_sys_label.place(relx=0.58, rely=0.25, anchor=W)
        self.eq_sys_value = Label(self,
                                  text=f"{self.obj.pretty_dict_print(sys, delim, ret=True)}",
                                  font=math_font,
                                  justify=LEFT)
        self.eq_sys_value.place(relx=0.58, rely=0.33, anchor=W)

        matrix, vect = self.obj.get_sys_coeffs()
        matrix = self.obj.round_matrix_coeffs(matrix, 2)
        self.coeff_matrix_label = Label(self,
                                        text="Матрица коэфф-ов системы ур-ий",
                                        font=titles_font,
                                        justify=LEFT)
        self.coeff_matrix_label.place(relx=0.58, rely=0.41, anchor=W)
        self.coeff_matrix_value = Label(self,
                                        text=f"{self.obj.pretty_matrix_print(matrix, ret=True)}",
                                        font=math_font,
                                        justify=LEFT)
        self.coeff_matrix_value.place(relx=0.58, rely=0.49, anchor=W)

        matrix, vect = self.obj.get_sys_coeffs()
        self.vector_label = Label(self,
                                  text="Вектор свободных членов",
                                  font=titles_font,
                                  justify=LEFT)
        self.vector_label.place(relx=0.58, rely=0.56, anchor=W)
        self.vector_value = Label(self,
                                  text=f"{vect}",
                                  font=math_font,
                                  justify=LEFT)
        self.vector_value.place(relx=0.58, rely=0.6, anchor=W)

        self.sys_roots_label = Label(self,
                                     text="Корни системы уравнений",
                                     font=titles_font,
                                     justify=LEFT)
        self.sys_roots_label.place(relx=0.58, rely=0.66, anchor=W)
        self.sys_roots_value = Label(self,
                                     text=f"{self.obj.get_sys_roots()}",
                                     font=math_font,
                                     justify=LEFT)
        self.sys_roots_value.place(relx=0.58, rely=0.7, anchor=W)
        sys = self.obj.generate_eq_sys(round_coeff=True, decimals=2)
        delim = " => "
        self.analityc_view_label = Label(self,
                                         text="Аналитическое выражение",
                                         font=titles_font,
                                         justify=LEFT)
        self.analityc_view_label.place(relx=0.58, rely=0.76, anchor=W)
        self.analityc_view_value = Label(self,
                                         text=f"{self.obj.get_analityc_view().split(' = ')[2]}",
                                         font=math_font,
                                         justify=LEFT)
        self.analityc_view_value.place(relx=0.58, rely=0.8, anchor=W)

        self.show_graph_button = ColoredButton(self,
                                               width=35,
                                               text="Отобразить график полученного решения",
                                               command=self.obj.visualize)
        self.show_graph_button.place(relx=0.5, rely=0.92, anchor=CENTER)
        symb = 60
        integral_sum_values_value_text = self.integral_sum_values_value.cget("text")
        print(integral_sum_values_value_text)
        common_integral_view_value_text = self.common_integral_view_value.cget("text")
        analytic_view_text = self.analityc_view_value.cget("text")
        if len(integral_sum_values_value_text) > 500:
            string = ""
            for i in range(len(integral_sum_values_value_text) // symb):
                string += f"{integral_sum_values_value_text[symb + symb * i:symb + 2 * symb * (i + 1)]}\n"
            self.integral_sum_values_value.config(text=string)
        if len(common_integral_view_value_text) > symb:
            string = ""
            for i in range(len(common_integral_view_value_text) // symb):
                string += f"{common_integral_view_value_text[symb + symb * i:symb + 2 * symb * (i + 1)]}\n"
            self.common_integral_view_value.config(text=string)
