def atbash(encoded_text):
    new_text = ""
    for item in encoded_text:
        new_text += unique_chars[alphabet_len - unique_chars.index(item) - 1]
    return new_text


with open('mumu.txt', 'r') as file:
    text = file.read()

unique_chars = sorted(set(text))
alphabet_len = len(unique_chars)
print(unique_chars)
print("Длинна алфавита", alphabet_len)

new_book = atbash(text)

with open('new_mumu.txt', 'w', encoding='Windows-1251') as file:
    encoded_file = file.write(new_book)

input("Нажмите Enter, чтобы декодировать...")
decoded_book = atbash(new_book)

with open('new_mumu.txt', 'w', encoding='Windows-1251') as file:
    decoded_file = file.write(decoded_book)
