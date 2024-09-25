from algorithm import *
import tkinter as tk
from tkinter import *

base_bg = "white"


# Кастомные кнопки управления.
class CustomButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,  # Remove button relief
            highlightthickness=0,  # Remove highlight
            padx=5,  # Add horizontal padding
            pady=5,  # Add vertical padding
            font=("Arial", 10),  # Set font
            foreground="black",  # Text color
            background=base_bg,  # Background color
            cursor="hand2"  # Hover cursor
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_click)

    # Наведение курсора на кнопку.
    def on_hover(self, event):
        self.config(background="gray")  # Change color on hover

    # Отведение курсора от кнопки.
    def on_leave(self, event):
        self.config(background=base_bg)  # Restore original color

    # Нажатие на кнопку.
    def on_click(self, event):
        self.config(bd=1, background=base_bg)


# Бзоаый класс интерфейса
class RedBlackTreeGUI:
    def __init__(self):
        self.rb_tree = RedBlackTree()
        self.root = self.rb_tree.root

        # Базовые настройки.
        self.root_window = tk.Tk()
        self.root_window.config(bg="#D3D3D3")
        self.root_window.title("RB - Tree")

        # Канвас для отрисовки дерева.
        self.canvas = tk.Canvas(self.root_window, width=800, height=450, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3)

        # Лейбл "Введите число".
        self.entry_label = Label(self.root_window, text="Введите число", font=("Arial", 11), background="#D3D3D3")
        self.entry_label.grid(row=3, column=0, columnspan=2, padx=(0, 0), pady=(10, 12))

        # Поле для ввода значения нового узла.
        self.entry = Entry(self.root_window, justify="center")
        self.entry.grid(row=4, column=0, columnspan=2, padx=50, sticky=NSEW)

        # Кнопка "Вставить".
        self.insert_button = CustomButton(self.root_window, text="Вставить", command=self.insert)
        self.insert_button.grid(row=3, column=2, padx=6, pady=12)

        # Кнопка "Удалить".
        self.delete_button = CustomButton(self.root_window, text="Удалить", command=self.delete)
        self.delete_button.grid(row=4, column=2, padx=6, pady=12)

        # Кнопка "Очистить".
        self.delete_button = CustomButton(self.root_window, text="Очистить", command=self.clear)
        self.delete_button.grid(row=5, column=2, padx=6, pady=12)

    # Callback для очищения дерева.
    def clear(self):
        self.rb_tree.reset()
        self.canvas.delete("all")
        self.update_tree_view(self.rb_tree.root, 400, 50, 200)

    # Callback для вставки.
    def insert(self):
        try:
            value = int(self.entry.get())
            self.rb_tree.insert(value)
            self.entry.delete(0, END)
            self.update_tree_view(self.rb_tree.root, 400, 50, 200)
        except ValueError:
            pass

    # Callback для удаления.
    def delete(self):
        try:
            value = int(self.entry.get())
            self.rb_tree.delete_node(value)
            self.entry.delete(0, END)
            self.canvas.delete("all")
            self.update_tree_view(self.rb_tree.root, 400, 50, 200)
        except ValueError:
            pass

    # Отрисовка листа.
    def draw_leaf(self, x, y):
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")
        self.canvas.create_text(x, y, text="null", fill="white")

    # Отрисовка узла.
    def draw_node(self, x, y, value, color):
        radius = 20
        text_color = "white" if color == "black" else "black"
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        self.canvas.create_text(x, y, text=str(value), fill=text_color, font=("Arial", 12, "bold"))

    # Отрисовка линии между узлами.
    def draw_edge(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2)

    # Отрисовка дерева.
    def update_tree_view(self, node, x, y, dx):
        if node and node.key != 0:
            color = "red" if node.color == "R" else "black"
            self.draw_node(x, y, node.key, color)

            delta_x_left, delta_y_left = -18, 7
            delta_x_right, delta_y_right = 18, 7

            if node.left and node.left.key != 0:
                x_left = x - dx
                y_left = y + 50
                self.draw_edge(x + delta_x_left, y + delta_y_left, x_left, y_left)
                self.update_tree_view(node.left, x_left, y_left, dx / 2)
            else:
                self.draw_leaf(x - dx, y + 50)
                self.draw_edge(x + delta_x_left, y + delta_y_left, x - dx, y + 50)  # Соединяем лист с родителем

            if node.right and node.right.key != 0:
                x_right = x + dx
                y_right = y + 50
                self.draw_edge(x + delta_x_right, y + delta_y_right, x_right, y_right)
                self.update_tree_view(node.right, x_right, y_right, dx / 2)
            else:
                self.draw_leaf(x + dx, y + 50)
                self.draw_edge(x + delta_x_right, y + delta_y_right, x + dx, y + 50)  # Соединяем лист с родителем

    # Запустить программу.
    def run(self):
        self.root_window.mainloop()


# Входная точка.
if __name__ == "__main__":
    rb_tree_gui = RedBlackTreeGUI()
    rb_tree_gui.run()
