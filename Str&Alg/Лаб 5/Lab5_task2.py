from straight import Stack
from linked import LinkedStack

print("Выбор реализации стека:\n",
      "1 - Прямой\n",
      "2 - Цепной (связанный)", sep="")
num = int(input())

if num == 1:

    print("1 - Создать стек")
    print("2 - Просмотреть элементы стека")
    print("3 - Добавить элемент в стек")
    print("4 - Удалить элемент стека")
    print("5 - Просмотреть последний элемент стека")
    print("6 - Проверить стек на пустоту")
    print("0 - Выйти")

    while True:

        inp = int(input())
        if inp == 1:
            stack = Stack()
            print("Стек создан и ожидает заполнения")
        elif inp == 2:
            try:
                print(stack.get_stack())
            except NameError:
                print("Стек не создан!")

        elif inp == 3:
            elem_to_add = int(input("Введите элемент:"))
            stack.add_elem(elem_to_add)
        elif inp == 4:
            stack.delete_elem()
        elif inp == 5:
            print(stack.read_elem())
        elif inp == 6:
            print(stack.is_empty())
        elif inp == 0:
            break

elif num == 2:
    print("1 - Создать стек")
    print("2 - Просмотреть элементы стека")
    print("3 - Добавить элемент в стек")
    print("4 - Удалить элемент стека")
    print("5 - Просмотреть последний элемент стека")
    print("6 - Проверить стек на пустоту")
    print("0 - Выйти")

    while True:

        inp = int(input())
        if inp == 1:
            stack = LinkedStack()
            print("Стек создан и ожидает заполнения")
        elif inp == 2:
            try:
                print(stack.get_stack())
            except NameError:
                print("Стек не создан!")
        elif inp == 3:
            elem_to_add = int(input("Введите элемент: "))
            stack.add_elem(elem_to_add)
        elif inp == 4:
            stack.delete_elem()
        elif inp == 5:
            print(stack.read_elem())
        elif inp == 6:
            print(stack.is_empty())

        elif inp == 0:
            break
