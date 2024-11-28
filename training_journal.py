import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import json
from datetime import datetime

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.beginning_period = ttk.Label(self.root, text="Начало периода:")
        self.beginning_period.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.beginning_period_value = ttk.Entry(self.root)
        self.beginning_period_value.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        self.end_period = ttk.Label(self.root, text="Окончание периода:")
        self.end_period.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.end_period_value = ttk.Entry(self.root)
        self.end_period_value.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        self.period = ttk.Button(self.root, text="Вывести период", command=self.view_records1)
        self.period.grid(column=2, row=5, columnspan=2)

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
        values_list_set = ["Без сортировки"] + list(values_list_set)
        # options_list = self.options_list  # Создание списка значений толщины
        self.value_inside = tk.StringVar()  # Переменная для отслеживания выбранного варианта в OptionMenu
        self.value_inside.set("Без сортировки")  # Установка значения по умолчанию для переменной
        # Создание виджета OptionMenu и передача ему созданного списка опций и переменной
        self.exercise = ttk.Label(self.root, text="Выбрать упражнение:")
        self.exercise.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.specific_exercise = tk.OptionMenu(self.root, self.value_inside, *values_list_set)
        self.specific_exercise.grid(column=1, row=7, columnspan=1)

    def view_records1(self):
        data = load_data()
        records_window = Toplevel(self.root)
        # records_window1 = Toplevel(self.root)
        records_window.title("Записи тренировок")
        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")
        try:
            dt1 = datetime.strptime(self.beginning_period_value.get(), '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime(self.end_period_value.get(), '%Y-%m-%d %H:%M:%S')
        except:
            dt1 = datetime.strptime('2020-10-28 00:00:00', '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime('2023-10-30 00:00:00', '%Y-%m-%d %H:%M:%S')
        for entry in data:

            dt3 = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
            if dt3 > dt1 and dt3 < dt2:
                tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        tree.pack(expand=True, fill=tk.BOTH)


    def add_entry(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self):
        data = load_data()
        records_window = Toplevel(self.root)
        # records_window1 = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        for entry in data:
            if self.value_inside.get() == 'Без сортировки':
                tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
            else:
                if entry['exercise'] == self.value_inside.get():
                    tree.insert('', tk.END,
                                values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        tree.pack(expand=True, fill=tk.BOTH)

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
