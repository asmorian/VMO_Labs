import random
import string
import re


# Task 1
def task_1():
    filename = "Lab2_task1.txt"
    with open(filename, "w") as file:
        for i in range(100):
            file.write(str(random.randint(-100, 100)))
            file.write("\n")

    counter = 0
    with open("Lab2_task1.txt", "r") as file:
        for number in file:
            if int(number) < 0:
                counter = counter + 1

    print("Кол-во отрицательных чисел =", counter, "\n")


# Task 2
def task_2(length, place, char):

    with open("Lab2_task2.txt", "w", encoding="utf-8") as file:
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        file.write(rand_string)

    with open("Lab2_task2.txt", "r", encoding="utf-8") as file2:
        character_string = str(file2.read())
        first_part = character_string[:place]
        second_part = character_string[place:len(character_string)]
        print("Строка до изменения: ", character_string)

        new_char_string = first_part + char + second_part
        with open("Lab2_task2.txt", "w", encoding="utf-8") as write_file:
            write_file.write(new_char_string)

    with open("Lab2_task2.txt", "r", encoding="utf-8") as file3:
        print("Строка после изменения:", str(file3.read()), "\n")


# Task 3
def task_3(num):

    line_num = 0
    with open("Lab2_task3.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line_num == num-1:
                print("Строка номер ", num, ":\n", sep="")
                print(line)
            line_num += 1

        if line_num < num-1:
            print("В файле меньше ", num, "строк", sep="")


# Task 4
def task_4(search_string):

    line_num = 1
    with open("Lab2_task4.txt", "r", encoding="utf-8") as file:
        for line in file:
            matching_plots = re.findall(search_string, line)

            if len(matching_plots) == 1:
                print("Номер строки:", line_num)
                print("Позиция вхождения:", line.find(search_string)+1)

            if len(matching_plots) > 1:
                print("Номер строки:", line_num)
                print("Количество вхождений:", len(matching_plots))
                pattern = re.compile(search_string)
                occurrences_found = pattern.finditer(line)
                counter = 1
                for m in occurrences_found:
                    print("Позиция вхождения ", counter, ": ", m.start() + 1, sep='')
                    counter += 1

            line_num += 1

    print("\n")


# Task 5
def task_5():

    file_object = {}
    filename = "Lab2_task5.txt"

    with open(filename, "r", encoding="utf-8") as file:
        file_contents = file.read()
        all_words = str(file_contents).split(" ")
        regex = "^[\n]+$"
        pat = re.compile(regex)
        for words in all_words:
            res = pat.search(words)
            if res:
                two_word = words.split("\n")
                all_words.remove(words)
                all_words.append(two_word[0])
                all_words.append(two_word[1])

        for word in all_words:
            if word not in file_object:
                file_object[word] = 1
            else:
                file_object[word] += 1

    print(file_object)


# task_1()
# task_2(10, 5, "_X_")
# task_3(50)
# task_4("имя")
# task_5()
