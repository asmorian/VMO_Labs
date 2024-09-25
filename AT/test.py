test = [1, 2, 3]
try:
    print(test[10])
except IndexError:
    print("Элемента с таким индексом нет")
