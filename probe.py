import matplotlib.pyplot as plt

# Предполагаем, что у вас есть данные x и y
x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 30, 25]

# Создаем столбчатый график
plt.bar(x, y, label='Величина прибыли')

# Функция для создания вертикальных надписей x
def add_vertical_labels(x, y):
    for i, (xi, yi) in enumerate(zip(x, y)):
        plt.text(xi, yi, str(i+1), rotation=90, ha='center', va='bottom')

# Добавляем вертикальные надписи x
add_vertical_labels(x, y)

# Добавляем легенду и заголовок
plt.legend()
plt.title('График величины прибыли')

# Отображаем график
plt.tight_layout()
plt.show()