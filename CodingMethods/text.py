file_path = "hp.txt"

# Открываем файл для чтения
with open(file_path, 'r') as file:
    content = file.read()

# Удаляем все одинарные кавычки
updated_content = content.replace(" ", " ")

# Открываем файл для записи и перезаписываем изменённое содержимое
with open(file_path, 'w') as file:
    file.write(updated_content)

print("Все одинарные кавычки удалены.")
