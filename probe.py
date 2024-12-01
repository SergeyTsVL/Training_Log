# import json
# import csv
#
# # Чтение JSON-файла
# with open('training_log.json', 'r') as json_file:
#     data = json.load(json_file)
#
# # Открытие файла для записи CSV
# with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
#
#     # Запись заголовков
#     writer.writeheader()
#
#     # Запись данных
#     for item in data:
#         writer.writerow(item)
#
# print("Данные успешно сохранены в CSV-файл.")
#
#
# import csv
# import json
#
# # Чтение CSV-файла
# with open('output.csv', 'r', newline='', encoding='utf-8') as csv_file:
#     reader = csv.DictReader(csv_file)
#
#     # Список для хранения данных
#     data = list(reader)
#
# # Запись данных в JSON-файл
# with open('training_log.json', 'w', encoding='utf-8') as json_file:
#     json.dump(data, json_file, ensure_ascii=False, indent=4)
#
# print("Данные успешно сохранены в JSON-файл.")


import csv
import json

# Чтение CSV-файла
with open('output.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    data = list(reader)
    print(data)
print(33333)
# Создаем словарь для сохранения данных в JSON
json_data = []
print(22222)
# Заполняем словарь данными из CSV
for row in data[1:]:  # Пропускаем заголовок
    print(row)
    json_data.append(
        {"data": row[0],
         "exercise": row[1],
         "weight": row[2],
         "repetitions": row[3]
         }
    )
print(json_data)
# Запись данных в JSON-файл
with open('training_log2.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в формат JSON.")