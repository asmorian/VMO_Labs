# Реализация сплошного представления списка

class ListItem:
    def __init__(self, value):
        self.value = value
        self.moves_count = 0
    
    def __repr__(self):
        if self.value == None:
            return "None"
        else:
            return f" {self.value}|{self.moves_count} "

    def add_val(self,val):
        self.value = val

    def add_count(self):
        self.moves_count += 1

    def clear(self):
        self.value = None
        self.moves_count = 0


class LinearList:
    def __init__(self, capacity):
        self.list = [ListItem(None) for _ in range(capacity)]
        self.capacity = capacity
        self.size = 0

    def add(self, value):
        if self.size < len(self.list):
            self.list[self.size] = ListItem(value)
            self.size += 1

        else:
            print("Список заполнен")

    def insert(self, value, index):
        if self.size == self.capacity:
            print("Место закончилось")
            return None

        if index >= 0 and index < self.capacity - 1:
            self.list.insert(index, ListItem(value))

            for i in range(index + 1 , self.size + 1):
                self.list[i].add_count()

        else:
            print("Некорректный индекс")

    def remove(self, index):
        if index >= 0 and index < self.size:
            for i in range(index, self.size - 1):
                self.list[i] = self.list[i + 1]
            self.list[self.size - 1] = ListItem(None)
            self.size -= 1

            for i in range(index , self.size):
                self.list[i].add_count()

        else:
            print("Некорректный индекс")

    def show(self):
        return self.list

    def clear(self):
        for i in range(len(self.list)):
            self.list[i].clear()


# Реализация цепного представления списка

class LinkedList:
    def __init__(self):
        self.list = []

    def add(self, value):
        self.list.append(value)
    
    def remove(self, value):
        self.list.remove(value)

    def insert(self, value, index):
        if index > len(self.list):
            print("Нельзя")
            return None
        else:
            self.list.insert(index, value)

    def show(self):
        return self.list