import tkinter.font
import customtkinter

from core.IntegralEquation import *

import matplotlib.colors as mcolors
from gui.screens.ResultScreen import ResultScreen as ResultScreenCLS
from gui.screens.ProgramScreen import *
from gui.custom.ColoredButton import *
from utilities.constants import *

from tkinter import ttk
from tkinter import filedialog as fd


# Класс интерфейса настроек аппроксимации.
class SettingsScreen(ProgramScreen):
    def __init__(self, parent, controller):
        ProgramScreen.__init__(self, parent, controller, self)
        # Тип уравнения
        self.eq_type = ""
        # Метод
        self.method = ""
        # Параметр интегрального ур-ия (лямбда)
        self.lmd = 0
        # Нижний предел интегрирования
        self.a = 0
        # Верхний предел интегрирования
        self.b = 0
        # Количество отрезков деления
        self.n = 2
        # Ядро интегрального ур-ия
        self.ks = ""
        # Известная функция
        self.fx = ""
        # Содержит переданные пользователем параметры
        self._entries_data = []

        # Дефолтный шрифт в полях ввода
        math_font = tkinter.font.Font(family="Cambria", size=10)

        # Тип уравнения
        self.eq_type_label = Label(self,
                                   text="Тип уравнения",
                                   font=("Arial Bold", 10))
        self.eq_type_label.place(relx=0.32, rely=0.25, anchor=CENTER)
        types = ["Фредгольма", "Вольтерра"]
        self.eq_type_drop = customtkinter.CTkOptionMenu(self,
                                                        values=types,
                                                        height=30,
                                                        width=170,
                                                        font=("Helvetica", 12),
                                                        fg_color="white",
                                                        dropdown_font=("Helvetica", 12),
                                                        corner_radius=50,
                                                        button_color="white",
                                                        button_hover_color="light grey",
                                                        dropdown_hover_color="light grey",
                                                        dropdown_fg_color="white",
                                                        dropdown_text_color="black",
                                                        text_color="black",
                                                        hover=True,
                                                        anchor="w",  # n-s-e-w-center
                                                        state="normal",
                                                        text_color_disabled="black",
                                                        dynamic_resizing=False,
                                                        )
        self.eq_type_drop.place(relx=0.32, rely=0.31, anchor=CENTER)

        # Используемый метод
        self.method_label = Label(self,
                                  text="Используемый метод",
                                  font=("Arial Bold", 10))
        self.method_label.place(relx=0.32, rely=0.4, anchor=CENTER)
        methods = ["Симпсона", "Трапеций"]
        self.method_drop = customtkinter.CTkOptionMenu(self,
                                                       values=methods,
                                                       height=30,
                                                       width=170,
                                                       font=("Helvetica", 12),
                                                       fg_color="white",
                                                       dropdown_font=("Helvetica", 12),
                                                       corner_radius=50,
                                                       button_color="white",
                                                       button_hover_color="light grey",
                                                       dropdown_hover_color="light grey",
                                                       dropdown_fg_color="white",
                                                       dropdown_text_color="black",
                                                       text_color="black",
                                                       hover=True,
                                                       anchor="w",  # n-s-e-w-center
                                                       state="normal",
                                                       text_color_disabled="black",
                                                       dynamic_resizing=False,
                                                       )
        self.method_drop.place(relx=0.32, rely=0.46, anchor=CENTER)

        # Параметр интегрольного уравнения (лямбда, λ)
        self.lmd_label = Label(self,
                               text="Параметр (лямбда, λ)",
                               font=("Arial Bold", 10))
        self.lmd_label.place(relx=0.32, rely=0.55, anchor=CENTER)
        self.lmd_entry = Entry(font=math_font)
        self.lmd_entry.place(relx=0.32, rely=0.61, anchor=CENTER)

        # Нижний предел интегрирования a
        self.lower_bound_label = Label(self,
                                       text="Нижний предел a",
                                       font=("Arial Bold", 10))
        self.lower_bound_label.place(relx=0.32, rely=0.7, anchor=CENTER)
        self.lower_bound_entry = Entry(font=math_font)
        self.lower_bound_entry.place(relx=0.32, rely=0.76, anchor=CENTER)

        # Верхний предел интегрирования
        self.upper_bound_label = Label(self,
                                       text="Верхний предел b",
                                       font=("Arial Bold", 10))
        self.upper_bound_label.place(relx=0.65, rely=0.25, anchor=CENTER)
        self.upper_bound_entry = Entry(font=math_font)
        self.upper_bound_entry.place(relx=0.65, rely=0.31, anchor=CENTER)

        # Кол-во разбиений отрезка интегрирования n.
        self.n_label = Label(self,
                             text="Разбиения отрезка n",
                             font=("Arial Bold", 10))
        self.n_label.place(relx=0.65, rely=0.4, anchor=CENTER)
        self.n_entry = Entry(font=math_font)
        self.n_entry.place(relx=0.65, rely=0.46, anchor=CENTER)

        # Ядро уравнения K(S)
        self.ks_label = Label(self,
                              text="Ядро уравнения K(S)",
                              font=("Arial Bold", 10))
        self.ks_label.place(relx=0.65, rely=0.55, anchor=CENTER)
        self.ks_entry = Entry(font=math_font)
        self.ks_entry.place(relx=0.65, rely=0.61, anchor=CENTER)

        # Функция f(x)
        self.fx_label = Label(self,
                              text="Функция f(x)",
                              font=("Arial Bold", 10))
        self.fx_label.place(relx=0.65, rely=0.7, anchor=CENTER)
        self.fx_entry = Entry(font=math_font)
        self.fx_entry.place(relx=0.65, rely=0.76, anchor=CENTER)

        self.solve_button = ColoredButton(self,
                                          width=20,
                                          text="Решить уравнение",
                                          command=self.run)
        self.solve_button.place(relx=0.28, rely=0.87, anchor=CENTER)
        self.clear_button = ColoredButton(self,
                                          width=20,
                                          text="Очистить содержимое",
                                          command=self.clear)
        self.clear_button.place(relx=0.68, rely=0.87, anchor=CENTER)

        # Сообщение пользователю.
        self.user_message = Label(self,
                                  font=("Arial Bold", 10))
        self.user_message.place(relx=0.02, rely=0.95, anchor=W)

    def process_entries_data(self):
        # Обработка всех полей с настройками.
        lmd = "err" if len(
            self.lmd_entry.get()) > 0 and not self.controller.is_float(self.lmd_entry.get()) or len(
            self.lmd_entry.get()) == 0 \
            else self.lmd_entry.get()

        lower_bound = "err" if len(
            self.lower_bound_entry.get()) > 0 and not self.controller.is_float(self.lower_bound_entry.get()) \
            else self.lower_bound_entry.get()

        upper_bound = "err" if len(
            self.upper_bound_entry.get()) > 0 and not self.controller.is_float(self.upper_bound_entry.get()) \
            else self.upper_bound_entry.get()

        n = "err" if len(
            self.n_entry.get()) > 0 and not self.controller.is_float(self.n_entry.get()) \
            else self.n_entry.get()

        ks = "err" if len(self.ks_entry.get()) == 0 else self.ks_entry.get()

        fx = "err" if len(self.fx_entry.get()) == 0 else self.fx_entry.get()

        # Пользовательские сообщения.
        if lmd == "err":
            self.user_message.configure(text="Параметр интегрального уравнения должен иметь вещественный тип!")

        if lower_bound == "err":
            self.user_message.configure(text="Нижний предел интегрирования должен иметь вещественный тип!", fg="red")

        if upper_bound == "err":
            self.user_message.configure(text="Верхний предел интегрирования должен иметь вещественный тип!", fg="red")

        if n == "err":
            self.user_message.configure(text="Количество разбиений отрезка n должно иметь тип целое число!", fg="red")

        if ks == "err":
            self.user_message.configure(text="Не введено ядро интегрального уравнения!", fg="red")

        if fx == "err":
            self.user_message.configure(text="Не введена известная функция!", fg="red")

        return {
            "eq_type": self.eq_type_drop.get(),
            "method": self.method_drop.get(),
            "lmd": lmd,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "n": n,
            "ks": ks,
            "fx": fx
        }

    def run(self, *args):
        # Получаем данные, введенные пользователем
        self._entries_data = self.process_entries_data()

        # Проверяет на корректное заполнение всех полей.
        for entry in self._entries_data:
            if self._entries_data[entry] == "err":
                return

        # Заполняем вводимые значения
        self.eq_type = self._entries_data["eq_type"]
        self.method = self._entries_data["method"]
        self.lmd = float(self._entries_data["lmd"])
        self.a = int(self._entries_data["lower_bound"])
        self.b = int(self._entries_data["upper_bound"])
        self.n = int(self._entries_data["n"])
        self.ks = self._entries_data["ks"]
        self.fx = self._entries_data["fx"]

        # Ошибок при вводе нет, сообщение пользователю пусто.
        self.user_message.configure(text="")

        # Запуск вычислений.
        eq_obj = IntegralEquation(self.eq_type, self.method, self.lmd, self.a, self.b, self.n, self.ks, self.fx)

        # Переходим на экран результатов, передавая все данные
        self.controller.show_frame(ResultScreenCLS, eq_obj)

    def show_entries(self):
        self.lmd_entry.place(relx=0.32, rely=0.6, anchor=CENTER)
        self.lower_bound_entry.place(relx=0.32, rely=0.75, anchor=CENTER)
        self.upper_bound_entry.place(relx=0.65, rely=0.3, anchor=CENTER)
        self.n_entry.place(relx=0.65, rely=0.45, anchor=CENTER)
        self.ks_entry.place(relx=0.65, rely=0.6, anchor=CENTER)
        self.fx_entry.place(relx=0.65, rely=0.75, anchor=CENTER)

    def hide_entries(self):
        self.lmd_entry.place_forget()
        self.lower_bound_entry.place_forget()
        self.upper_bound_entry.place_forget()
        self.n_entry.place_forget()
        self.ks_entry.place_forget()
        self.fx_entry.place_forget()

    def clear(self, *args):
        self.user_message.configure(text="")
        self.lmd_entry.delete(0, END)
        self.lower_bound_entry.delete(0, END)
        self.upper_bound_entry.delete(0, END)
        self.n_entry.delete(0, END)
        self.ks_entry.delete(0, END)
        self.fx_entry.delete(0, END)
