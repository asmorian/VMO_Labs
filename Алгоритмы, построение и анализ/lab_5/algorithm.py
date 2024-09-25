# Класс "Узел".
class Node:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


# Класс "AVL-дерево".
class AVLTree:

    # Получить высоту дерева.
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Обновить высоту дерева.
    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # Получить текущий баланс дерева (разницу между высотой левого и правого поддеревьев)
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Сбалансировать по правой стороне.
    def rotate_right(self, y):
        x = y.left
        T = x.right

        x.right = y
        y.left = T

        self.update_height(y)
        self.update_height(x)

        return x

    # Сбалансировать по левой стороне.
    def rotate_left(self, x):
        y = x.right
        T = y.left

        y.left = x
        x.right = T

        self.update_height(x)
        self.update_height(y)

        return y

    # Общий метод для балансировки дерева.
    def rebalance(self, node):
        self.update_height(node)

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # Вставка узла в дерево.
    def insert(self, root, key):
        if not root:
            return Node(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        return self.rebalance(root)

    # Удаление узла из дерева.
    def delete(self, root, key):
        if not root:
            return

        elif key < root.key:
            root.left = self.delete(root.left, key)

        elif key > root.key:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        return self.rebalance(root)

    # Получить узел с минимальным значением.
    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root

        return self.get_min_value_node(root.left)

    # Очистить дерево.
    def delete_root(self, root):
        root = None

    # Рекурсивный обход дерева.
    def inorder_traversal(self, root):
        if root:
            self.inorder_traversal(root.left)
            self.inorder_traversal(root.right)


def main():
    avl_tree = AVLTree()
    root = None

    while True:
        try:
            value = int(input("Введите число для добавления в дерево (для завершения введите 'q'): "))
            root = avl_tree.insert(root, value)
            avl_tree.inorder_traversal(root)
        except ValueError:
            break


