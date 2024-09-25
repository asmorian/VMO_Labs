import sys


# Класс узла.
class Node:
    def __init__(self, key, parent=None, color="R"):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.color = color


# Класс красно-чёрного дерева.
class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.root = self.TNULL

    # Функция для вставки узла
    def insert(self, key):
        # Обычная вставка для BST
        node = Node(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "R"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        # y - родительской узел
        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        # Если новый узел - корень дерева, то его цвет красный
        if node.parent == None:
            node.color = "B"
            return

        # Если дедушка - None, то пропускаем
        if node.parent.parent == None:
            return

        # Балансировка дерева после вставки
        self.fix_insert(node)

    # Функция для балансировки красно-черного дерева после вставки нового узла
    def fix_insert(self, k):
        while k.parent.color == "R":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == "R":
                    # case 3.1
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # case 3.2.2
                        k = k.parent
                        self.right_rotate(k)
                    # case 3.2.1
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == "R":
                    # mirror case 3.1
                    u.color = "B"
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    k = k.parent.parent  # x now must be a black node
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = "B"
                    k.parent.parent.color = "R"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "B"

    # Функции для удаления узла
    def delete_node(self, key):
        z = self.TNULL
        node = self.root
        while node != self.TNULL:
            if node.key == key:
                z = node

            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "B":
            self.fix_delete(x)

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def fix_delete(self, x):
        while x != self.root and x.color == "B":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "R":
                    # case 3.1
                    s.color = "B"
                    x.parent.color = "R"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "B" and s.right.color == "B":
                    # case 3.2
                    s.color = "R"
                    x = x.parent
                else:
                    if s.right.color == "B":
                        # case 3.3
                        s.left.color = "B"
                        s.color = "R"
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = "B"
                    s.right.color = "B"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "R":
                    # case 3.1
                    s.color = "B"
                    x.parent.color = "R"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "B" and s.right.color == "B":
                    # case 3.2
                    s.color = "R"
                    x = x.parent
                else:
                    if s.left.color == "B":
                        # case 3.3
                        s.right.color = "B"
                        s.color = "R"
                        self.left_rotate(s)
                        s = x.parent.left

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = "B"
                    s.left.color = "B"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "B"

    # Функции для поворотов
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Поиск минимального узла
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    # Вспомогательная функция для вывода дерева
    def print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            print(str(node.key) + "(" + node.color + ")")
            self.print_helper(node.left, indent, False)
            self.print_helper(node.right, indent, True)

    # Вывод дерева
    def print_tree(self):
        self.print_helper(self.root, "", True)

    # Очистка.
    def reset(self):
        self.root = None
        self.TNULL = Node(0)
        self.root = self.TNULL


# Пример использования
if __name__ == "__main__":
    bst = RedBlackTree()
