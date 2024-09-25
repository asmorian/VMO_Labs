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
    def add(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
        else:
            current_node = self.root
            while True:
                if value < current_node.value:
                    if current_node.left is None:
                        current_node.left = new_node
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = new_node
                        break
                    else:
                        current_node = current_node.right

    def delete(self, value):
        def delete_node(node, value):
            if node is None:
                return None
            if value == node.value:
                # удаляем узел
                if node.left is None and node.right is None:
                    return None
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                temp_node = node.right
                while temp_node.left:
                    temp_node = temp_node.left
                node.value = temp_node.value
                node.right = delete_node(node.right, temp_node.value)
            elif value < node.value:
                node.left = delete_node(node.left, value)
            else:
                node.right = delete_node(node.right, value)
            return node

        self.root = delete_node(self.root, value)
# Запрос выбора режима ввода
mode = input("Выберите режим ввода данных ('1' - ввод с клавиатуры, '2' - ввод из файла): ")

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
    exit()

# Бесконечный цикл для добавления/удаления элементов и вывода дерева
while True:
    operation = input("Выберите операцию ('1' - добавление элемента, '2' - удаление элемента, '0' - выход из программы): ")

    # Добавление элемента
    if operation == '1':
        element = int(input("Введите элемент для добавления: "))
        bst.insert(element)
        bst.print_tree()

    # Удаление элемента
    elif operation == '2':
        element = int(input("Введите элемент для удаления: "))
        bst.delete(element)
        bst.print_tree()

    # Выход из программы
    elif operation == '0':
        exit()

    # Некорректный выбор операции
    else:
        print("Некорректный выбор операции.")
