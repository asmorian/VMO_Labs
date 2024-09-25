class Stack:
    def __init__(self):
        self.array = []

    def add_elem(self, elem):
        self.array.append(elem)

    def delete_elem(self):
        if self.is_empty():
            return "Стек пустой. Нельзя удалить"
        else:
            self.array.pop()

    def read_elem(self):
        if self.is_empty():
            return "Стек пустой нельзя прочитать"
        else:
            return self.array[-1]
        
    def get_stack(self):
        return self.array
    
    def is_empty(self):
        if len(self.array) == 0:
            return True
        else:
            return False

"""
stack = Stack()
stack.add_elem("a")
stack.add_elem("b")
stack.add_elem("c")
stack.add_elem("d")
stack.add_elem("e")

print(stack.get_stack())
print(stack.read_elem())

stack.delete_elem()
print(stack.get_stack())
print(stack.read_elem())

stack.delete_elem()
stack.delete_elem()
stack.delete_elem()

print(stack.is_empty())

stack.delete_elem()
stack.delete_elem()

print(stack.is_empty())
"""