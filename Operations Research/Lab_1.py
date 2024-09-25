import flet
import numpy as np
import simp


def string_to_list(number_string):
    # Удаляем пробелы, разделяем строку по запятым и преобразуем каждый элемент в число
    return [int(num.strip()) for num in number_string.split(',')]


def main(page: flet.Page):
    # Настройка окна
    page.title = 'Lab_1'
    page.theme_mode = 'dark'
    page.vertical_alignment = flet.MainAxisAlignment.START
    page.window.width = 360
    page.window.height = 600

    # Создание переменных виджетов
    a_enter = flet.TextField('2, 3, 3', border_color='lightblue', width=250)
    b_enter = flet.TextField('1, 6, 7', border_color='lightblue', width=250)
    t_enter = flet.TextField('438, 747, 812', border_color='lightblue', width=250)
    r_enter = flet.TextField('4, 5', border_color='lightblue', width=250)

    max_profit_text = flet.Text(value="")
    sol_A = flet.Text(value="")
    sol_B = flet.Text(value="")

    def button_click(e):
        a = string_to_list(a_enter.value)
        b = string_to_list(b_enter.value)
        c = string_to_list(r_enter.value)
        for i in range(len(c)):
            c[i] = - c[i]

        A = []
        for i in range(len(a)):
            A.append([a[i], b[i]])

        A = np.array(A)
        T = np.array([string_to_list(t_enter.value)])

        solution, max_profit = simp.simplex(c, A, T)

        # Обновляем текстовые поля
        max_profit_text.value = f"{max_profit}"
        sol_A.value = f"{solution[0]}"
        sol_B.value = f"{solution[1]}"

        # Обновляем страницу
        page.update()

    page.add(
        flet.Row([
            flet.Column([
                flet.Row([
                    flet.Text('Начальные данные:', weight=flet.FontWeight.BOLD)
                ],
                    alignment=flet.MainAxisAlignment.START),
                flet.Row([
                    flet.Text('A', weight=flet.FontWeight.BOLD, width=10),
                    a_enter

                ],
                    alignment=flet.MainAxisAlignment.START),
                flet.Row([
                    flet.Text('B', weight=flet.FontWeight.BOLD, width=10),
                    b_enter

                ],
                    alignment=flet.MainAxisAlignment.START),
                flet.Row([
                    flet.Text('t', weight=flet.FontWeight.BOLD, width=10),
                    t_enter,
                ],
                    alignment=flet.MainAxisAlignment.START),
                flet.Row([
                    flet.Text('r', weight=flet.FontWeight.BOLD, width=10),
                    r_enter,
                    flet.IconButton(flet.icons.UPLOAD, on_click=button_click)
                ],
                    alignment=flet.MainAxisAlignment.START),
                flet.Divider(color='white'),
                flet.Row([
                    flet.Text('Вывод:', weight=flet.FontWeight.BOLD),
                ]),
                flet.Row([
                    flet.Text('Прибыль:', weight=flet.FontWeight.BOLD),
                    max_profit_text
                ]),
                flet.Row([
                    flet.Text('Кол-во A:', weight=flet.FontWeight.BOLD),
                    sol_A
                ]),
                flet.Row([
                    flet.Text('Кол-во B:', weight=flet.FontWeight.BOLD),
                    sol_B
                ]),
            ])
        ])

    )


flet.app(target=main)
