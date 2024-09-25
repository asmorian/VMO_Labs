class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedStack:
    def __init__(self):
        self.top = None  # Вершина стека

    def is_empty(self):
        if self.top is None:
            print("Стек пуст!")
            return False
        else:
            return True

    def add_elem(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def delete_elem(self):
        if self.is_empty() is False:
            print("Элемент не был удалён, так как стек пуст!")
            return None
        deleted_elem = self.top.data
        self.top = self.top.next
        return deleted_elem

    def read_elem(self):
        if self.is_empty():
            return None
        return self.top.data

    def get_stack(self):
        current = self.top
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


"""
# Пример использования
stack = LinkedStack()

stack.add_elem(1)
stack.add_elem(2)
stack.add_elem(3)

print("Стек после добавления элементов:", end=' ')
stack.display()

print("Элемент на вершине стека:", stack.read_elem())
print("Извлекаем элементы из стека:", stack.delete_elem(), stack.delete_elem())

print("Стек после извлечения элементов:", end=" ")
stack.display() 
"""
