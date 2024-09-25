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

    def search(self, key, use_barrier=False, lower_barrier=None, upper_barrier=None):
        comparisons = 0  # счетчик числа сравнений
        current = self.root
        while current is not None:
            if use_barrier:
                if lower_barrier is not None and key < lower_barrier:
                    return None, comparisons
                if upper_barrier is not None and key > upper_barrier:
                    return None, comparisons
            comparisons += 1
            if key == current.value:
                return current, comparisons
            elif key < current.value:
                current = current.left
            else:
                current = current.right
        return None, comparisons

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

    # Запрос выбора метода поиска
    search_method = input("Выберите метод поиска ('1' - без барьера, '2' - с барьером): ")

    # Поиск без барьера
    if search_method == '1':
        key = int(input("Введите ключ для поиска: "))
        result, comparisons = bst.search(key)
        if result is not None:
            print(f"Значение {key} найдено в дереве.")
        else:
            print(f"Значение {key} не найдено в дереве.")
        print(f"Число сравнений: {comparisons}")

    # Поиск с барьером
    elif search_method == '2':
        use_barrier = input("Вы точно хотите использовать барьер? 1 - да, 2 - нет: ")
        if use_barrier.lower() == '1':
            lower_barrier = int(input("Введите нижнюю границу: "))
            upper_barrier = int(input("Введите верхнюю границу: "))
        else:
            lower_barrier = None
            upper_barrier = None
        key = int(input("Введите ключ для поиска: "))
        result, comparisons = bst.search(key, lower_barrier=lower_barrier, upper_barrier=upper_barrier)
        if result is not None:
            print(f"Значение {key} найдено в дереве.")
        else:
            print(f"Значение {key} не найдено в дереве.")
        print(f"Число сравнений: {comparisons}")
# Ввод данных из файла
elif mode == '2':
    bst = BinarySearchTree()
    file_name = input("Введите имя файла: ")
    with open(file_name, 'r') as f:
        elements = f.readline().split()
        elements = [int(e) for e in elements]
        for element in elements:
            bst.insert(element)
    bst.print_tree()

    # Запрос выбора метода поиска
    search_method = input("Выберите метод поиска ('1' - без барьера, '2' - с барьером): ")

    # Поиск без барьера
    if search_method == '1':
        key = int(input("Введите ключ для поиска: "))
        result, comparisons = bst.search(key)
        if result is not None:
            print(f"Значение {key} найдено в дереве.")
        else:
            print(f"Значение {key} не найдено в дереве.")
        print(f"Число сравнений: {comparisons}")

    # Поиск с барьером
    elif search_method == '2':
        use_barrier = input("Вы точно хотите использовать барьер? 1 - да, 2 - нет: ")
        if use_barrier.lower() == '1':
            lower_barrier = int(input("Введите нижний барьер: "))
            upper_barrier = int(input("Введите верхний барьер: "))
        else:
            lower_barrier = None
            upper_barrier = None
        key = int(input("Введите ключ для поиска: "))
        result, comparisons = bst.search(key, use_barrier=use_barrier, lower_barrier=lower_barrier, upper_barrier=upper_barrier)
        if result is not None:
            print(f"Значение {key} найдено в дереве.")
        else:
            print(f"Значение {key} не найдено в дереве.")
        print(f"Число сравнений: {comparisons}")
