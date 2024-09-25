from classes import LinkedList, LinearList


def linear():
    print("Введите размер списка")
    size = int(input(">> "))
    l = LinearList(size)

    print("1 - Добавить элемент в список")
    print("2 - Удалить элемент из списка")
    print("3 - Отобразить список")
    print("4 - Вставить элемент по индексу")
    print("6 - Отчистить")
    print("5 - Выйти из программы")

    while True:
        inp = int(input(">>> "))
        if inp == 1:
            val = int(input("Введите значение >> "))
            l.add(val)
        if inp == 2:
            idx = int(input("Введите индекс >> "))
            l.remove(idx)
        if inp == 3:
            print(l.show())
        if inp == 4:
            ins = input("Введите значение и индекс через пробел >> ").split(" ")
            l.insert(int(ins[0]), int(ins[1]))
        if inp == 5:
            break
        if inp == 6:
            l.clear()


def linked():
    l = LinkedList()
    print("Введите 1 чтобы добавить элемент в список")
    print("Введите 2 чтобы удалить элемент из списка")
    print("Введите 3 чтобы отобразить список")
    print("Введите 4 чтобы вставить элемент по индексу")
    print("Введите 5 чтобы выйти из программы")

    while True:
        inp = int(input(">>> "))

        if inp == 1:
            val = int(input("Введите значение >> "))
            l.add(val)

        if inp == 2:
            vall = int(input("Введите значение для удаления >> "))
            l.remove(vall)

        if inp == 3:
            print(l.show())

        if inp == 4:
            ins = input("Введите значение и индекс через пробел >> ").split(" ")
            l.insert(int(ins[0]), int(ins[1]))

        if inp == 5:
            break


print("Введите 1 для работы с сплошным и 2 для работы с цепным представлением")
inp = int(input(">>> "))
if inp == 1:
    linear()
if inp == 2:
    linked()

