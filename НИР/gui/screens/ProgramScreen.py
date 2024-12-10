# Работа с Excel-таблицей
import openpyxl
import pandas as pd

# Модуль интерфейса.
from tkinter import *

# Библиотека цветов модуля matplotlib.
import matplotlib.colors as mc


class ProgramScreen(Frame):
    def __init__(self, parent, controller, screen):
        Frame.__init__(self, parent)
        self.controller = controller
        self.colors = mc.CSS4_COLORS

        self.main_label = Label(self,
                                text="Решение интегральных уравнений",
                                font=("Arial Bold", 14))
        self.main_label.place(relx=0.5, rely=0.08, anchor=CENTER)

    def is_color_supported(self, color):
        return color in list(self.colors.keys()) or color in list(self.colors.values())

    def print_colors_table(self):
        print(pd.DataFrame.from_dict({
            "Словесное описание": list(self.colors.keys()),
            "HEX-представление": list(self.colors.values())
        }))
    def clear(self):
        pass
