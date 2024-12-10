from Lab_2_1 import *
import time


# Сканируем файл и выводим его длину, а так же его битовую форму
def scan_file(file_name):
    with open(file_name, 'r') as file:
        text = file.read()

    text_len = len(text)
    print(f"Символов в тексте: {text_len}")

    byte_file = text.encode('windows-1251')
    return byte_file, text_len


# Создаем ключ генерации случайного числа и сохраняем его в файле
def create_key():
    a, b, c, = not_rand_rand(uptime)
    with open('key.txt', 'w') as file:
        file.write(str(a) + '\n')
        file.write(str(b) + '\n')
        file.write(str(c) + '\n')
        file.close()


# Создаем гамму для наложения на основе ключа генерации и длины исходного текста
def create_gamma(key, text_len):
    with open(key, 'r') as file:
        keys_file = file.readlines()

    # Считываем значения ключа
    if len(keys_file) == 3:
        a = int(keys_file[0])
        b = int(keys_file[1])
        c = int(keys_file[2])

    # Либо используем стандартный ключ
    else:
        print("Файл ключ записан не корректно, будут использованы параметры по умолчанию\n"
              "a = 490\n"
              "b = 24500\n"
              "X_0 = 50490")

        a = 490
        b = 24500
        c = 50490

    # Длинна генерируемой последовательности берётся на основе длины текста, делённого на среднюю длину генерируемого числа
    num_of_nums = text_len // 7
    nums = psd_num(a, b, c, m, num_of_nums)

    # Превращаем последовательность чисел в большую строку цифр
    string_nums = ''
    for item in nums:
        string_nums += str(item)

    nums_len = len(string_nums)

    # Проверяем, достаточна ли длинна
    if nums_len < text_len:
        temp = text_len - nums_len
        temp = nums - temp
        string_nums += string_nums[temp:]

    # Если да, то делаем срез до длинны текста и кодируем
    gamma = string_nums[:text_len]
    gamma = gamma.encode('windows-1251')

    return gamma


# Наложение гаммы на текст. На вход должны получить два текста в нужной кодировке (в данном случае windows-1251)
def encode(text, gamma):
    # По битам ксорим символы из text & gamma, после чего записываем результат и декодируем его обратно из битовой формы в обычную строку
    result = bytes([b1 ^ b2 for b1, b2 in zip(text, gamma)])
    result = result.decode('windows-1251', errors='ignore')

    return result


# Менюшка пользователя
def handle_choice(choice):
    match choice:
        case "1":
            create_key()
            print('Ключ успешно создан!')
        case "2":

            # Тут получаем имена файла и проверяем корректность, после чего кодируем и сохраняем файл
            try:
                file_name = str(input('Введите имя кодируемого файла: '))
                utf_file, file_len = scan_file(file_name)

                new_file_name = str(input('Введите имя нового файла: '))
                start_time = time.time()
                gamma = create_gamma('key.txt', file_len)

                with open(new_file_name, "w") as file:

                    file.write(encode(utf_file, gamma))
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"Время выполнения гаммирования: {execution_time} секунд")

                    file.close()
            except FileNotFoundError:
                print("Неверное имя файла, попробуйте снова")
        case "3":
            print("Выход из программы.")
            return False
        case _:
            print("Неверный выбор. Попробуйте снова.")
    return True


def show_menu():
    print("\n--- Главное меню ---")
    print("1. Создать ключ генерации")
    print("2. Закодировать файл")
    print("3. Выход")


if __name__ == "__main__":
    while True:
        show_menu()
        users_choice = input("Введите номер опции: ")
        if not handle_choice(users_choice):
            break
