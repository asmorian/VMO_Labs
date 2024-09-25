class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.front = None  # Начало очереди
        self.rear = None   # Конец очереди

    def is_empty(self):
        return self.front is None

    def add_elem(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def delete_elem(self):
        if self.is_empty():
            return None
        removed_data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return removed_data

    def read_elem(self):
        if self.is_empty():
            return None
        return self.front.data

    def get_queue(self):
        current = self.front
        while current:
            print(current.data, end=' ')
            current = current.next
        print()

"""
queue = LinkedQueue()

queue.add_elem(1)
queue.add_elem(2)
queue.add_elem(3)

print("Очередь после добавления элементов:")
queue.get_queue()

print("Извлекаем элементы из очереди:")
print(queue.delete_elem())
print(queue.delete_elem())

print("Очередь после извлечения элементов:")
queue.get_queue()
"""