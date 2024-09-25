def custom_sort(pl, inf_mode, reverse=False):
    if inf_mode == "inf_in_str":
        l_infs = []
        l_noinfs = []

        # Разделение элементов на содержащие "inf" и не содержащие
        for item in pl:
            if "inf" in item:
                l_infs.append(item)
            else:
                l_noinfs.append(item)

        # Функция для сортировки списков с "inf"
        def inf_sort_key(row):
            inf_count = row.count("inf")
            sum_without_inf = sum([x for x in row if x != "inf"])
            return (inf_count, sum_without_inf)

        # Сортировка
        sorted_pl_infs = sorted(l_infs, key=inf_sort_key, reverse=reverse)
        sorted_pl_noinfs = sorted(l_noinfs, key=lambda row: sum(row), reverse=reverse)

        # Объединение отсортированных списков
        sorted_pl = sorted_pl_infs + sorted_pl_noinfs

        # Удаление "inf" и преобразование
        t = [[sorted_pl[i][j] for j in range(len(sorted_pl[i])) if sorted_pl[i][j] != "inf"] for i in
             range(len(sorted_pl))]
        t = list(map(lambda x: list(set(x))[0], t))

        return sorted_pl, t


# Пример использования функции
pl = [
    [12, 12, 'inf', 'inf'],
    [13, 13, 13, 13],
    [17, 17, 17, 17],
    ['inf', 17, 17, 17],
    [15, 'inf', 15, 'inf'],
    [19, 'inf', 19, 'inf'],
    [13, 13, 13, 13],
    [15, 'inf', 15, 15],
    [15, 15, 15, 15],
    [14, 'inf', 14, 14],
    [20, 20, 20, 'inf'],
    [10, 10, 10, 10]
]

sorted_pl, t = custom_sort(pl, "inf_in_str", reverse=True)
print("Sorted List with 'inf':")
for row in sorted_pl:
    print(row)
print("\nList t (without 'inf'):")
print(t)
