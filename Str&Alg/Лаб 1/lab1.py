import string


# Описание множества.
def create_set(*elems):
    if len(elems) == 0:
        return set()
    elif len(elems) == 1:
        return set(list(*elems))
    elif len(elems) > 1:
        return {*elems}


# Процедура вывода множества.
def printset(primes):
    length = len(primes)
    elems = list(primes)

    print("Число элементов в множестве:", length)
    print("Элементы множества:", elems)


# Задания 1.
def task_1():
    print("-------Задание 1--------")
    set_A = create_set(1, 2, 3, 4, 4, 6)
    printset(set_A)


# Задание 2.
def task_2():
    print("-------Задание 2--------")
    set_B = create_set()
    value = input("Введите значения множества: ")
    set_B.add(value)

    while True:
        value = input("Введите значения множества: ")
        if value == "-":
            break
        set_B.add(value)

    printset(set_B)


# Задание 3.
def task_3():
    print("-------Задание 3--------")
    stmt1 = "Язык является полностью объектно-ориентированным в том плане, что всё является объектами"
    stmt2 = "Сам же язык известен как интерпретируемый и используется в том числе для написания скриптов"

    words_stmt1_set = create_set(stmt1.split(" "))
    words_stmt2_set = create_set(stmt2.split(" "))

    common_words = create_set()

    for word_stmt1 in words_stmt1_set:
        for words_stmt2 in words_stmt2_set:
            if word_stmt1 in words_stmt2_set:
                common_words.add(word_stmt1)

    print("Первое множество со словами:", words_stmt1_set)
    print("Второе множество со словами:", words_stmt2_set)
    print("Общие слова:", common_words)


# Задание 4
def task_4():
    print("-------Задание 4--------")
    set_S = create_set("f", 9, 4, "А", "d", 8, "г", "q", "Щ", "J", 6, 6, 9, "W", "И", "т")

    latin_symbols = create_set(string.ascii_letters)
    cyrillic_symbols = create_set("АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя")
    digits = create_set(string.digits)

    set_A = create_set()
    set_B = create_set()
    set_C = create_set()

    for elem in set_S:
        if elem in latin_symbols:
            set_A.add(elem)
        if elem in cyrillic_symbols:
            set_B.add(elem)
        if str(elem) in digits:
            set_C.add(elem)

    print("Множество A:", set_A)
    print("Множество B:", set_B)
    print("Множество C:", set_C)


task_1()
task_2()
task_3()
task_4()
