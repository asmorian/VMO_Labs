from algorithm import *
import tkinter as tk
import operator
from tkinter import *

base_bg = "white"
w = 1000
h = 1000


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
            cursor="hand2",  # Hover cursor
            bd=2,
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_click)

    # Наведение курсора на кнопку.
    def on_hover(self, event):
        self.config(background="grey")  # Change color on hover

    # Отведение курсора от кнопки.
    def on_leave(self, event):
        self.config(background=base_bg)  # Restore original color

    # Нажатие на кнопку.
    def on_click(self, event):
        self.config(bd=1, background=base_bg)


# Базовый класс интерфейса
class BTreeGUI:
    def __init__(self):
        self.B_tree = BTree(3)
        self.root = None

        # Базовые настройки.
        self.root_window = tk.Tk()
        self.root_window.config(bg="#D3D3D3")
        self.root_window.title("B - Tree ")

        # get screen width and height
        self.ws = self.root_window.winfo_screenwidth()  # width of the screen
        self.hs = self.root_window.winfo_screenheight()  # height of the screen

        # set the dimensions of the screen
        self.root_window.geometry(f"{self.ws}x{self.hs}")

        # Канвас для отрисовки дерева.
        self.canvas = tk.Canvas(self.root_window, width=self.ws, height=self.hs - 380, bg=base_bg)
        self.canvas.grid(row=1, column=0, columnspan=4)

        # Лейбл "Введите порядок дерева:".
        self.order_label = Label(self.root_window, text="Введите порядок дерева", font=("Arial", 11),
                                 background="#D3D3D3")
        self.order_label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        # Поле для ввода порядка дерева
        self.entry_tree_order = Entry(self.root_window, justify="center")
        self.entry_tree_order.grid(row=3, column=0, columnspan=1,  padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.entry_tree_order.bind("<Return>", self.createTreeButtonEnter)

        # Кнопка "Создать дерево"
        self.create_btree_button = CustomButton(text="Создать дерево", command=self.create_btree)
        self.create_btree_button.grid(row=2, column=1, columnspan=1, pady=15)

        # Лейбл "Введите значения ключей:".
        self.entry_label = Label(self.root_window, text="Введите значения ключей", font=("Arial", 11),
                                 background="#D3D3D3")
        self.entry_label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

        # Поле для ввода значения нового узла.
        self.insert_node_tree = Entry(self.root_window, state=DISABLED, justify="center")
        self.insert_node_tree.grid(row=5, column=0, columnspan=1, padx=(10, 10), pady=(10, 10), sticky=NSEW)
        self.insert_node_tree.bind("<Return>", self.insertKeyEntryEnter)

        # Кнопка "Вставить".
        self.insert_button = CustomButton(text="Вставить", command=self.insert_node)
        self.insert_button.grid(row=2, column=2, pady=15)

        # Скрытые поля ввода.
        self.del_key = Entry(self.root_window, state=DISABLED)

        # Кнопка "Удалить".
        self.delete_button = CustomButton(text="Удалить", command=self.delete_node, state=DISABLED)
        self.delete_button.grid(row=3, column=2, pady=15)

        # Кнопка "Отобразить".
        self.show_btree_button = CustomButton(text="Отобразить", command=self.show_btree, state=DISABLED)
        self.show_btree_button.grid(row=4, column=2, pady=15)

        # Кнопка "Очистить".
        self.clear_button = CustomButton(text="Очистить", command=self.clear, state=DISABLED)
        self.clear_button.grid(row=5, column=2, pady=15)

    # Press Enter Callbacks
    def createTreeButtonEnter(self, *args):
        self.create_btree()

    def insertKeyEntryEnter(self, *args):
        self.insert_node()

    # Очистка.
    def clear(self):
        self.B_tree.clear()
        self.insert_node_tree.delete(0, END)
        self.insert_node_tree.config(state=DISABLED)
        self.entry_tree_order.config(state=NORMAL)
        self.create_btree_button.config(state=NORMAL)
        self.entry_tree_order.delete(0, END)
        self.canvas.delete("all")

    # Функция для создания B-дерева
    def create_btree(self):
        try:
            order = int(self.entry_tree_order.get())
            global B
            B = BTree(order)
            self.show_btree_button["state"] = "disabled"
            self.entry_tree_order["state"] = "disabled"
            self.insert_node_tree.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)
            self.del_key.config(state=NORMAL)
            self.delete_button.config(state=NORMAL)
        except ValueError:
            pass

    # Функция для вставки узла в B-дерево
    def insert_node(self):
        try:
            key = int(self.insert_node_tree.get())
            self.B_tree.insert((key, 2 * key))
            self.insert_node_tree.delete(0, END)
            self.show_btree_button.config(state=NORMAL)
            self.clear_button.config(state=NORMAL)
            self.create_btree_button.config(state=DISABLED)
        except ValueError:
            pass

    # Функция для отображения B-дерева на canvas
    def display_btree(self):
        self.delete_button.config(state=NORMAL)
        self.canvas.delete("all")
        self.B_tree.print_tree(self.B_tree.root)

    # Функция для рисования B-дерева на canvas
    def show_btree(self):
        self.canvas.delete("all")
        self.insert_node_tree.delete(0, END)
        self.draw_tree(self.B_tree.root, (self.ws / 2) - 20, 50, 200)

    # Функция для удаления узла.
    def delete_node(self):
        key = int(self.insert_node_tree.get())
        self.B_tree.delete(self.B_tree.root, [key, 2 * key])

    # Рекурсивная функция для рисования узлов и связей B-дерева
    def draw_tree(self, node, x, y, spacing):
        self.canvas.create_rectangle(x - 20, y - 10, x + 20, y + 10, fill="white")
        self.canvas.create_text(x, y, text=" ".join(str(i[0]) for i in node.keys), fill="black")
        if not node.leaf:
            for i, child in enumerate(node.child):
                child_x = x + (i - len(node.child) // 2) * spacing
                child_y = y + 50
                self.canvas.create_line(x, y + 10, child_x, child_y - 10)
                self.draw_tree(child, child_x, child_y, spacing // len(node.child))

    # Запустить программу.
    def run(self):
        self.root_window.mainloop()


# Входная точка.
if __name__ == "__main__":
    B_tree_gui = BTreeGUI()
    B_tree_gui.run()
