import tkinter as tk
from tkinter import ttk


def longest_common_subsequence(X, Y):
    m = len(X)
    n = len(Y)

    # Создаем матрицу для хранения результатов подзадач
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Заполняем матрицу с использованием динамического программирования
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Восстанавливаем наибольшую общую подпоследовательность
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs)), dp


def new_win(value):
    resp_win = tk.Tk()
    resp_win.title("Ответ")
    resp_win.geometry("200x70")
    resp_text = ttk.Label(resp_win, text="Ответ:")
    resp_text2 = ttk.Label(resp_win, text=value)
    resp_text.pack()
    resp_text2.pack()


def button_clicked():
    matrix_win = tk.Tk()
    X = list_entry.get()
    Y = list2_entry.get()
    res, matrix = (longest_common_subsequence(X, Y))
    new_win(res)
    MatrixDisplay(matrix_win, matrix)


class MatrixDisplay:
    def __init__(self, master, matrix):
        self.master = master
        self.master.title("Matrix Display")

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.display_matrix(matrix)

    def display_matrix(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])

        cell_size = 25

        for i in range(rows):
            for j in range(cols):
                value = str(matrix[i][j])
                x = j * cell_size
                y = i * cell_size
                self.canvas.create_text(x + cell_size/2, y + cell_size/2, text=value)

        canvas_width = cols * cell_size
        canvas_height = rows * cell_size

        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))


# Окно
main_win = tk.Tk()
main_win.title("Поиск подпоследовательностей")
main_win.geometry("300x150")

list_label = ttk.Label(main_win, text="Введите последовательность 1")
list_label.pack()

list_entry = ttk.Entry()
list_entry.pack()

list2_label = ttk.Label(main_win, text="Введите последовательность 2")
list2_label.pack()

list2_entry = ttk.Entry()
list2_entry.pack()

create_button = tk.Button(main_win, text="Рассчитать", command=button_clicked)
create_button.pack()

main_win.mainloop()
