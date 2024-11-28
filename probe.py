import json

# Определяем путь к JSON-файлу
json_path = 'training_log.json'

# Создаем пустой список для хранения значений
values_list = []

# Читаем JSON-файл
with open(json_path, 'r', encoding='utf-8') as file:
    # Загружаем данные из файла в словарь
    data = json.load(file)
    # print(data)
for i in data:
    i.keys()
    # print(i['exercise'])
    values_list.append(i['exercise'])
values_list_set = set(values_list)
print(list(values_list_set))
# Проходим циклом по ключам и значениям в словаре
# for key, value in data.items():
#     # Здесь вы можете добавить условие для выбора значений
#     if isinstance(value, list):  # Если значение - список
#         values_list.extend(value)
#     elif isinstance(value, dict):  # Если значение - словарь
#         values_list.append(key)  # Добавляем ключ (или другое условие)
#
# # Выводим результат
# print(values_list)