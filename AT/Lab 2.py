# 1 Метод - (0*10*10)+ - 1 кратны 2
# 2 Метод - (1*01*01*01*)+ -  0 кратны 3


# На входе получаем один из двух методов построения и количество требуемых слов
def new_Word(regular_num, num_of_words):
    i = 0   # счетчик готовых слов
    match regular_num:
        case 1:                                                 # Если выбран метод 1
            start = 0                                           # Начальное число приравниваем к 0
            while i < num_of_words:                             # Пока кол-во написанных слов меньше требуемого, делаем:
                bin_start = bin(start)                          # Приводим число в бинарный формат вида "0dXXX"
                if "1" in bin_start[2:] and bin_start.count("1") % 2 == 0:   # Считаем кол-во единиц в записи числа, если оно кратно 2, то:
                    print(bin_start[2:])                        # Выводим число на экран, делая срез (Чтобы убрать 0d)
                    i += 1                                      # Добавляем к счетчику слов единичку
                start += 1                                      # Добавляем единичку к числу, которое будет потом бинарным
        case 2:
            start = 0
            while i < num_of_words:
                bin_start = bin(start)
                if "0" in bin_start[2:] and bin_start[2:].count("0") % 3 == 0:  # Тут тоже самое, но заранее отсекаем
                    print(bin_start[2:])                                        # указатель на бинарность, чтобы 0 не
                    i += 1                                                      # считался лишний раз и делим на 3
                start += 1


new_Word(1, 10)
print("-------------")
new_Word(2, 10)
