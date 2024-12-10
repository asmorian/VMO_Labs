from tkinter import *

# Экраны приложения.
from gui.screens.SettingsScreen import SettingsScreen as SettingsScreenCLS
from gui.screens.ResultScreen import ResultScreen as ResultScreenCLS


class GUI(Tk):
    def __init__(self, width, height, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Размеры окна.
        self.width = width
        self.height = height

        # Базовые настройки окна.
        self.title("Решение интегральных уравнений Фредгольма и Вольтерра 2-го рода")

        # Задаем иконку.
        self.icon = PhotoImage(file="images/calculator.png")
        self.iconphoto(False, self.icon)

        # Задаем размеры окна.
        self.set_geometry(self.width, self.height)

        # Создание базового контейнера.
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Словарь для хранения объектов страниц приложения.
        self.frames = {}

        # Кортеж всех страниц приложения.
        self.screens = (SettingsScreenCLS,
                        ResultScreenCLS)

        # Начальный экран.
        self.start_screen = SettingsScreenCLS

        # Запуск начального экрана.
        self.show_frame(self.start_screen)

    def set_geometry(self, w, h):
        # Ширина/высота экрана на устройстве.
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # Координаты Tkinter-окна.
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # Расположение окна на экране.
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def is_start_screen(self, screen):
        return screen == self.start_screen

    def back_to_settings(self, *args):
        self.set_geometry(self.width, self.height)
        self.frames[ResultScreenCLS].forget()
        self.frames[SettingsScreenCLS].tkraise()
        self.frames[SettingsScreenCLS].show_entries()

    def show_frame(self, scr, data=""):
        frame = ""
        cont = scr

        if cont == ResultScreenCLS:
            frame = cont(self.container, self, data)
            if SettingsScreenCLS in self.frames:
                self.frames[SettingsScreenCLS].hide_entries()
        else:
            frame = cont(self.container, self)

        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.clear()
        frame.tkraise()

    @staticmethod
    def is_float(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def iter_over_screens(self):
        for frame in self.frames:
            print(frame)

    def run(self):
        self.mainloop()
