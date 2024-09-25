from q_straight import Queue
from q_linked import LinkedQueue


print("Выбор реализации очереди:\n",
      "1 - Прямой\n",
      "2 - Цепной (связанный)", sep="")
num = int(input())

if num == 1:
    print("1 - Создать очередь")
    print("2 - Просмотреть элементы очереди")
    print("3 - Добавить элемент в очередь")
    print("4 - Получить элемент вершины очереди")
    print("5 - Проверить пустая ли очередь")
    print("6 - Удалить элемент")
    print("0 - Выйти")

    while True:
        inp = int(input())
        if inp == 1:
            q = Queue()
            print("Очередь создана и ожидает заполнения")
        elif inp == 2:
            try:
                print(q.get_queue())
            except NameError:
                print("Очередь не создана!")
        elif inp == 3:
            elem = int(input("Введите элемент: "))
            q.add_elem(elem)
        elif inp == 4:
            print(q.read_elem())
        elif inp == 5:
            print(q.is_empty())
        elif inp == 6:
            print(q.delete_elem())
        elif inp == 7:
            break

elif num == 2:
    print("1 - Создать очередь")
    print("2 - Просмотреть элементы очереди")
    print("3 - Добавить элемент в очередь")
    print("4 - Получить элемент вершины очереди")
    print("5 - Проверить пустая ли очередь")
    print("6 - Удалить элемент")
    print("0 - Выйти")

    while True:
        inp = int(input())
        if inp == 1:
            q = LinkedQueue()
            print("Очередь создана и ожидает заполнения")
        elif inp == 2:
            try:
                print(q.get_queue())
            except NameError:
                print("Очередь не создана!")
        elif inp == 3:
            elem = int(input("Введите элемент: "))
            q.add_elem(elem)
        elif inp == 4:
            print(q.read_elem())
        elif inp == 5:
            print(q.is_empty())
        elif inp == 6:
            print(q.delete_elem())
        elif inp == 7:
            break
