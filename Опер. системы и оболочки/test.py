import tkinter as tk
from tkinter import ttk


class CarDatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Database App")

        # Создаем фрейм для кнопок и таблицы
        self.frame = ttk.Frame(self.master)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Создаем кнопку для запуска отображения таблицы
        self.show_table_button = ttk.Button(self.frame, text="Показать таблицу", command=self.show_table)
        self.show_table_button.grid(row=0, column=0, padx=5, pady=5)

    def show_table(self):
        # Создаем Treeview для отображения данных
        columns = ("Марка", "Модель", "Год выпуска")
        car_tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        # Устанавливаем заголовки для столбцов
        for col in columns:
            car_tree.heading(col, text=col)

        # Пример добавления данных (замените этот блок кода на вашу логику)
        data = [("Toyota", "Camry", 2022),
                ("Honda", "Accord", 2021),
                ("Ford", "Mustang", 2023)]

        for row in data:
            car_tree.insert("", "end", values=row)

        # Размещаем таблицу в том же фрейме
        car_tree.grid(row=1, column=0, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDatabaseApp(root)
    root.mainloop()
