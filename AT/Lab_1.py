# Ввод размерности алфавита
n = int(input("Введите количество символов в алфавите: "))
alphabet = []

# Ввод символов алфавита, без повтора
for i in range(n):
    char = input("Введите буквы алфавита: ")
    while char in alphabet:
        print("Эта буква уже есть в алфавите! Введите другую букву:")
        char = input("Введите букву алфавита: ")
    alphabet.append(char)

# Вывод алфавита
print("Алфавит:", alphabet)

# Выбор действия
action = 0
while action != "1" and action != "2" and action != "3":
    action = input("---------------------"
                   "\nВыберите действие:"
                   "\n1 - Получить слово по порядковому номеру"
                   "\n2 - Получить порядковый номер слова"
                   "\n3 - Выйти "
                   "\n----> ")

# Действие 1 - Поиск по номеру

    if action == "1":
        word = ''
        remains_list = []
        num_list = []
        number = int(input("Введите номер: "))
        print("Введённый номер:", number)
        if 0 < number <= n:
            remains_list.append(number)
        while number > n:
            if number % n == 0:
                number = (number // n) - 1
                num_list.append(number)
                remains_list.append(n)
            else:
                remains_list.append(number % n)
                number = number // n
                num_list.append(number)
            if 0 < number <= n:
                remains_list.append(number)

        print("Массив целых:", num_list,
              "\nМассив остатков:", remains_list, end="\n")
        remains_list.reverse()
        word = []
        for i in range(len(remains_list)):
            word.append(alphabet[remains_list[i] - 1])
        word = ''.join(word)
        print("Слово:", word)

    if action == "2":
        word = list(input("Введите слово: "))
        print(word)
        remains_list = []
        for char in word:
            remains_list.append(alphabet.index(char) + 1)
        print("Массив остатков:", remains_list)
        number = int()
        remains_list.reverse()
        for i in range(len(remains_list)):
            number += remains_list[i] * n**i
        print("Номер слова:", number)

