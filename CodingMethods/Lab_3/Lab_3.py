from CodingMethods.Lab_3.DES import *
import random
import codecs

codecs.register_error('replace_with_space', lambda e: ('_', e.start + 1))


def scan_text_file(file_name):
    with open(file_name, "r", encoding='windows-1251') as file:
        text = file.read()

    binary_sequence = string2bin(text)
    return binary_sequence


def bin2string(binary_sequence):
    text = ''.join(
        chr(int(binary_sequence[i:i + 8], 2))
        for i in range(0, len(binary_sequence), 8)
    ).encode('latin1').decode('windows-1251', errors='replace_with_space')
    return text


def string2bin(text):
    binary_sequence = ''.join(format(byte, '08b') for byte in text.encode('windows-1251'))
    return binary_sequence


def split_into_blocks(byte_str):
    counter = 0
    temp = ""
    blocks = []

    for char in byte_str:
        if counter != 64:
            counter += 1
            temp += char
        else:
            blocks.append(temp)
            temp = ""
            counter = 1
            temp += char

    blocks.append(temp)

    if len(blocks[-1]) != 64:
        while len(blocks[-1]) != 64:
            blocks[-1] += "0"
    return blocks


def generate_binary_key():
    with open(file='binary_key.txt', mode='w') as file:
        key1 = ''.join(random.choice('01') for _ in range(64))
        key2 = ''.join(random.choice('01') for _ in range(64))
        file.write(key1)
        file.write('\n')
        file.write(key2)


def get_key_from_file(file_name):
    with open(file_name, 'r') as file:
        key = file.readlines()
    return key[0], key[1]


def triple_DES_encode(file_name, key1, key2):
    print("Получаем данные из файла...")
    bin_text = scan_text_file(file_name)
    blocks = split_into_blocks(bin_text)
    rkb1 = generate_keys(key1)
    rkb2 = generate_keys(key2)
    rkb1_rev = rkb1[::-1]
    rkb2_rev = rkb2[::-1]

    print("Шаг 1 - Кодируем с первым ключом")
    with open('steps/step1.txt', 'w') as file:
        for item in blocks:
            file.write(encrypt(item, rkb1))
        file.flush()

    print("Шаг 2 - Декодируем со вторым ключом")
    with open('steps/step1.txt', 'r') as file:
        hex_text = file.read()
    bin_text = hex2bin(hex_text)
    step2_blocks = split_into_blocks(bin_text)

    with open('steps/step2.txt', 'w') as file:
        for item in step2_blocks:
            file.write(encrypt(item, rkb2_rev))
        file.flush()

    print("Шаг 3 - Кодируем с первым ключом")
    with open('steps/step2.txt', 'r') as file:
        hex_text = file.read()
    bin_text = hex2bin(hex_text)
    step3_blocks = split_into_blocks(bin_text)

    with open('steps/step3.txt', 'w') as file:
        for item in step3_blocks:
            file.write(encrypt(item, rkb1))
        file.flush()

    print("Возвращаем в формат текста...")
    with open('steps/step3.txt', 'r') as file:
        encoded_hex = file.read()

    decoded_bin = hex2bin(encoded_hex)
    encoded = bin2string(decoded_bin)
    with open('encoded_Mumu.txt', 'w') as file:
        file.write(encoded)
        file.flush()

    # Декодирование
    s = input("Декодировать файл? (y/n) --> ")
    if s == ('y' or 'yes' or 'yeah' or 'да'):
        print("Шаг 4 - Декодируем с первым ключом")

        with open('steps/step3.txt', 'r') as file:
            hex_text = file.read()
            file.flush()
        bin_text = hex2bin(hex_text)
        step4_blocks = split_into_blocks(bin_text)

        # bin_text = scan_text_file('encoded_Mumu.txt')
        # step4_blocks = split_into_blocks(bin_text)

        with open('steps/step4.txt', 'w') as file:
            for item in step4_blocks:
                file.write(encrypt(item, rkb1_rev))
            file.flush()

        print("Шаг 5 - Кодируем со вторым ключом")
        with open('steps/step4.txt', 'r') as file:
            hex_text = file.read()
            file.flush()
        bin_text = hex2bin(hex_text)
        step5_blocks = split_into_blocks(bin_text)

        with open('steps/step5.txt', 'w') as file:
            for item in step5_blocks:
                file.write(encrypt(item, rkb2))
            file.flush()

        print("Шаг 6 - Декодируем с первым ключом")
        with open('steps/step5.txt', 'r') as file:
            hex_text = file.read()
            file.flush()
        bin_text = hex2bin(hex_text)
        step6_blocks = split_into_blocks(bin_text)

        with open('steps/step6.txt', 'w') as file:
            for item in step6_blocks:
                file.write(encrypt(item, rkb1_rev))
            file.flush()

        print("Возвращаем в формат текста...")
        with open('steps/step6.txt', 'r') as file:
            decoded_hex = file.read()
            file.flush()

        decoded_bin = hex2bin(decoded_hex)
        result = bin2string(decoded_bin)
        with open('result.txt', 'w') as file:
            file.write(result)
            file.flush()

    with (open("steps/step1.txt", "w"), open("steps/step2.txt", "w"),
          open("steps/step3.txt", "w"), open("steps/step4.txt", "w"),
          open("steps/step5.txt", "w"), open("steps/step6.txt", "w")):
        pass


if __name__ == "__main__":
    generate_binary_key()
    first_key, second_key = get_key_from_file('binary_key.txt')
    triple_DES_encode('Mumu.txt', first_key, second_key)
