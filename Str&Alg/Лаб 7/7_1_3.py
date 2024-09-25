class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            current = self.root
            while True:
                if value == current.value:
                    print(f"Значение {value} уже присутствует в дереве.")
                    break
                elif value < current.value:
                    if current.left is None:
                        current.left = Node(value)
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = Node(value)
                        break
                    else:
                        current = current.right

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root, "", True)

    def _print_tree(self, current_node, prefix, is_left):
        if current_node.right is not None:
            self._print_tree(current_node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(current_node.value))
        if current_node.left is not None:
            self._print_tree(current_node.left, prefix + ("    " if is_left else "│   "), True)

# Запрос выбора режима ввода
mode = input("Выберите режим ввода данных ('1' - ввод с клавиатуры, '2' - ввод из файла): ")

# Ввод данных с клавиатуры
if mode == '1':
    bst = BinarySearchTree()
    elements = input("Введите элементы через пробел: ").split()
    elements = [int(e) for e in elements]
    for element in elements:
        bst.insert(element)
    bst.print_tree()
# Чтение данных из файла
elif mode == '2':
    bst = BinarySearchTree()
    filename = input("Введите имя файла: ")
    with open(filename, 'r') as file:
        data = file.read().split()
    elements = [int(e) for e in data]
    for element in elements:
        bst.insert(element)
    bst.print_tree()

# Некорректный выбор режима ввода
else:
    print("Некорректный выбор режима ввода данных.")
# 7 6 8 1 3 5 4 2 9 12 10 7
