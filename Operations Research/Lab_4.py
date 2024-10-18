from cvxopt.modeling import variable, op
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox, scrolledtext

def solve_optimization():
    try:
        # Получаем входные данные
        c = list(map(int, entry_coeffs.get().split(',')))
        post = list(map(int, entry_supply.get().split(',')))
        potr = list(map(int, entry_demand.get().split(',')))

        # Инициализация переменных
        x = variable(15, 'x')
        z = sum(c[i] * x[i] for i in range(15))

        # Ограничения
        constraints = [
            (x[0] + x[1] + x[2] + x[3] + x[4] <= post[0]),
            (x[5] + x[6] + x[7] + x[8] + x[9] <= post[1]),
            (x[10] + x[11] + x[12] + x[13] + x[14] <= post[2]),
            (x[0] + x[5] + x[10] == potr[0]),
            (x[1] + x[6] + x[11] == potr[1]),
            (x[2] + x[7] + x[12] == potr[2]),
            (x[3] + x[8] + x[13] == potr[3]),
            (x[4] + x[9] + x[14] == potr[4]),
            (x >= 0)
        ]

        # Определение задачи
        problem = op(z, constraints)
        problem.solve(solver='glpk')

        # Создание таблицы результатов
        table = PrettyTable()
        table.field_names = ['Индекс', 'Значение']

        for i, value in enumerate(x.value):
            table.add_row([i + 1, value])

        # Отображение результата
        result_text = f'Результат:\n {table}\nСтоимость доставки: {problem.objective.value()[0]}'
        text_area.delete(1.0, tk.END)  # Очищаем текстовое поле
        text_area.insert(tk.END, result_text)  # Вставляем новый результат

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Создание интерфейса
root = tk.Tk()
root.title("Оптимизация транспортной задачи")

# Ввод коэффициентов
label_coeffs = tk.Label(root, text="Введите матрицу коэффициентов через запятую:")
label_coeffs.pack()
entry_coeffs = tk.Entry(root, width=50)
entry_coeffs.pack()

# Ввод запасов
label_supply = tk.Label(root, text="Введите запасы груза поставщиков через запятую:")
label_supply.pack()
entry_supply = tk.Entry(root, width=50)
entry_supply.pack()

# Ввод потребностей
label_demand = tk.Label(root, text="Введите запасы груза для потребителей через запятую:")
label_demand.pack()
entry_demand = tk.Entry(root, width=50)
entry_demand.pack()

# Кнопка для решения задачи
button_solve = tk.Button(root, text="Решить", command=solve_optimization)
button_solve.pack()

# Текстовое поле для отображения результатов
text_area = scrolledtext.ScrolledText(root, width=60, height=25, wrap=tk.WORD)
text_area.pack()

# Запуск главного цикла Tkinter
root.mainloop()


# 5, 2, 3, 6, 1, 1, 1, 4, 4, 2, 4, 1, 2, 3, 5
# 100, 300, 220
# 110, 200, 90, 100, 120
