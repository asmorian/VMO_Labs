import numpy as np


def simplex(c, A, b):
    # Добавляем slack переменные для преобразования ограничений неравенств в равенства
    m, n = A.shape
    A = np.hstack([A, np.eye(m)])
    c = np.hstack([c, np.zeros(m)])

    # Таблица симплекс-метода
    tableau = np.hstack([A, b.reshape(-1, 1)])
    tableau = np.vstack([tableau, np.hstack([c, 0])])

    # Симплекс-итерации
    while np.any(tableau[-1, :-1] < 0):
        # Определяем входную переменную (столбец с минимальным коэффициентом в строке Z)
        pivot_col = np.argmin(tableau[-1, :-1])

        # Определяем выходную переменную (по правилу минимального положительного отношения)
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        ratios[ratios <= 0] = np.inf  # Игнорируем отрицательные или нулевые элементы
        pivot_row = np.argmin(ratios)

        # Поворот (нормализуем опорный элемент)
        pivot = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot

        # Обновляем другие строки
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Получаем решение
    solution = np.zeros(n)
    for i in range(n):
        col = tableau[:, i]
        if np.count_nonzero(col[:-1]) == 1 and np.sum(col[:-1]) == 1:
            solution[i] = tableau[np.where(col[:-1] == 1)[0], -1][0]

    max_profit = tableau[-1, -1]
    return solution, max_profit


if __name__ == "__main__":
    # Пример данных (можно заменить своими)
    r1 = 4  # Прибыль за автомобиль A
    r2 = 5  # Прибыль за автомобиль B
    c = np.array([-r1, -r2])  # Для минимизации используем отрицательные коэффициенты

    a1, a2, a3 = 3, 3, 2  # Часы на оборудование для A
    b1, b2, b3 = 2, 3, 5  # Часы на оборудование для B
    t1, t2, t3 = 273, 300, 380  # Доступное время на каждом оборудовании

    A = np.array([
        [a1, b1],  # Ограничение по 1-му типу оборудования
        [a2, b2],  # Ограничение по 2-му типу оборудования
        [a3, b3]  # Ограничение по 3-му типу оборудования
    ])

    b = np.array([t1, t2, t3])  # Правая часть ограничений

    # Решение задачи
    solution, max_profit = simplex(c, A, b)

    # Вывод результатов
    print(f"Максимальная прибыль: {max_profit}")
    print(f"Количество автомобилей модели A: {solution[0]}")
    print(f"Количество автомобилей модели B: {solution[1]}")
