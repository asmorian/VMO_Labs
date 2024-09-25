class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def add_elem(self, item):
        self.items.append(item)

    def delete_elem(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def read_elem(self):
        if self.is_empty():
            return None
        return self.items[0]

    def get_queue(self):
        return self.items

"""
q = Queue()
q.add(1)
q.add(2)
q.add(3)
print(q.get_queue())
print(q.dell())
print(q.get_queue())
print(q.dell())
print(q.get_queue())
print(q.is_empty())
"""