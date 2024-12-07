import csv
import tkinter as tk
from textwrap import wrap
from tkinter import ttk, Toplevel, messagebox, filedialog, RIGHT, BOTTOM
import json
from datetime import datetime
from tkinter import *
import matplotlib.pyplot as plt

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self, values_list=[]):
        """
        Виджеты для ввода данных в виде полей ввода и кнопок на начальном окне.
        :param values_list:
        :return:
        """
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
        self.period = ttk.Button(self.root, text="Вывести период", command=self.period_records)
        self.period.grid(column=2, row=5, columnspan=2)
        self.enter_csv = ttk.Button(self.root, text="Экспорт csv", command=self.save_csv_file)
        self.enter_csv.grid(column=0, row=8)
        self.importing_csv = ttk.Button(self.root, text="Импорт csv", command=self.importing_csv_file)
        self.importing_csv.grid(column=1, row=8)
        # Читаем JSON-файл
        with open(data_file, 'r', encoding='utf-8') as file:
            # Загружаем данные из файла в словарь
            data = json.load(file)
        for i in data:
            i.keys()
            values_list.append(i['exercise'])
        values_list_set = set(values_list)
        values_list_set = ["Без сортировки"] + list(values_list_set)
        self.value_inside = tk.StringVar()  # Переменная для отслеживания выбранного варианта в OptionMenu
        self.value_inside.set("Без сортировки")  # Установка значения по умолчанию для переменной
        # Создание виджета OptionMenu и передача ему созданного списка опций и переменной
        self.exercise = ttk.Label(self.root, text="Выбрать упражнение:")
        self.exercise.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
        self.specific_exercise = tk.OptionMenu(self.root, self.value_inside, *values_list_set)
        self.specific_exercise.grid(column=1, row=7, columnspan=1)

    def period_records(self):
        """
        Метод выводит все сохраненные значения из training_log.json файла за указанный период.
        :return:
        """
        data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")
        self.tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")
        # Создает боковую прокрутку таблицы по вертикали
        game_scroll = Scrollbar(records_window)
        current_columns = game_scroll.grid_size()[0]
        game_scroll.grid(row=0, column=current_columns + 1, sticky="ns")
        # Проверяет наличие данных для периода, если нет то вводим значение по умолчанию
        try:
            dt1 = datetime.strptime(self.beginning_period_value.get(), '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime(self.end_period_value.get(), '%Y-%m-%d %H:%M:%S')
        except:
            messagebox.showinfo("Так не пойдет!!!", ' Файл должен быть формата\n %Y-%m-%d %H:%M:%S '
                                                    'по умолчанию:\n Начало периода: 2020-10-28 00:00:00'
                                                    '\n Окончание периода: 2024-12-30 00:00:00')
            dt1 = datetime.strptime('2020-10-28 00:00:00', '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime('2024-12-30 00:00:00', '%Y-%m-%d %H:%M:%S')
        # Выводим данные за период во всплывающее окно
        for entry in data:
            if self.value_inside.get() == 'Без сортировки':
                dt3 = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                if dt3 > dt1 and dt3 < dt2:
                    self.tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
            else:
                if entry['exercise'] == self.value_inside.get():
                    dt3 = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                    if dt3 > dt1 and dt3 < dt2:
                        self.tree.insert('', tk.END, values=(
                        entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        self.tree.grid(row=0, column=0)
        # Устанавливаем виджеты во всплывающее окно, привязываем к ним методы
        self.playerdate = Label(records_window, text="Дата")
        self.playerdate.grid(row=1, column=0, sticky=tk.W, padx=45, pady=5)
        self.playerdate_entry = Entry(records_window)
        self.playerdate_entry.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.playerexercise = Label(records_window, text="Упражнение")
        self.playerexercise.grid(row=1, column=0, sticky=tk.W, padx=160)
        self.playerexercise_entry = Entry(records_window)
        self.playerexercise_entry.grid(row=2, column=0, sticky=tk.W, padx=120)
        self.playerweight = Label(records_window, text="Вес")
        self.playerweight.grid(row=1, column=0, sticky=tk.W, padx=280)
        self.playerweight_entry = Entry(records_window)
        self.playerweight_entry.grid(row=2, column=0, sticky=tk.W, padx=240)
        self.playerrepetitions = Label(records_window, text="Повторения")
        self.playerrepetitions.grid(row=1, column=0, sticky=tk.W, padx=400)
        self.playerrepetitions_entry = Entry(records_window)
        self.playerrepetitions_entry.grid(row=2, column=0, sticky=tk.W, padx=360)
        self.select_button = Button(records_window, text="Выбрать строку", command=self.select_record)
        self.select_button.grid(row=3, column=0, sticky=tk.W, padx=5)
        self.edit_button = Button(records_window, text="Сохранить изменения", command=self.update_record)
        self.edit_button.grid(row=3, column=0, sticky=tk.W, padx=120)
        self.edit_button = Button(records_window, text="Удалить запись", command=self.delite_record)
        self.edit_button.grid(row=3, column=0, sticky=tk.W, padx=280)
        self.gen_diagram = Button(records_window, text="Диаграмма периода", command=self.general_diagram_period)
        self.gen_diagram.grid(row=3, column=0, sticky=tk.W, padx=400)

    def select_record(self):
        """
        Выделяем данные в строке и переносим их для редактирования
        :return:
        """
        # clear entry boxes
        self.playerdate_entry.delete(0, END)
        self.playerexercise_entry.delete(0, END)
        self.playerweight_entry.delete(0, END)
        self.playerrepetitions_entry.delete(0, END)
        # grab record
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        # output to entry boxes
        self.playerdate_entry.insert(0, values[0])
        self.playerexercise_entry.insert(0, values[1])
        self.playerweight_entry.insert(0, values[2])
        self.playerrepetitions_entry.insert(0, values[3])

    def update_record(self, update_list=[]):
        """
        Сохраняем изменения в редактируемой строке в training_log.json файл
        :param update_list:
        :return:
        """
        selected = self.tree.focus()
        values_record = self.tree.item(selected, text="",
                                       values=(self.playerdate_entry.get(), self.playerexercise_entry.get(),
                                               self.playerweight_entry.get(), self.playerrepetitions_entry.get()))
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        j = 0
        for i in data:
            if self.playerdate_entry.get() == i['date']:
                update_list.append({
                    'date': self.playerdate_entry.get(),
                    'exercise': self.playerexercise_entry.get(),
                    'weight': self.playerweight_entry.get(),
                    'repetitions': self.playerrepetitions_entry.get()
                })
            else:
                update_list.append({
                    'date': data[j]['date'],
                    'exercise': data[j]['exercise'],
                    'weight': data[j]['weight'],
                    'repetitions': data[j]['repetitions']
                })
            j += 1
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(update_list, f, indent=4)

    def delite_record(self):
        """
        Удаляем данные в строке и в training_log.json файле. Строка очищается.
        :return:
        """
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        delite_list = []
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        j = 0
        for i in data:
            delite_list.append({
                'date': data[j]['date'],
                'exercise': data[j]['exercise'],
                'weight': data[j]['weight'],
                'repetitions': data[j]['repetitions']
            })
            if values[0] == i['date']:
                del delite_list[j]
            j += 1
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(delite_list, f, indent=4)

        self.tree.item(selected, text="", values=(self.playerdate_entry.get(), self.playerexercise_entry.get(),
                                                  self.playerweight_entry.get(), self.playerrepetitions_entry.get()))
        self.playerdate_entry.delete(0, END)
        self.playerexercise_entry.delete(0, END)
        self.playerweight_entry.delete(0, END)
        self.playerrepetitions_entry.delete(0, END)

    def add_entry(self):
        """
        Вносим данные в поля на начальной строке, при этом проверяем их. Проверка на положительность чисел,
        и заполнение всех строк. Далее эти строки сохраняются в training_log.json файле, а сами строки очищаются.
        :return:
        """
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        try:
            if int(self.weight_entry.get()) >= 0:
                weight = int(self.weight_entry.get())
            else:
                messagebox.showerror("Ошибка при вводе 'ВЕС'", "Должны быть положительные числа")
        except:
            messagebox.showerror("Ошибка при вводе 'ВЕС'", "Должны быть числа")
        try:
            if int(self.repetitions_entry.get()) >= 0:
                repetitions = int(self.repetitions_entry.get())
            else:
                messagebox.showerror("Ошибка при вводе 'ПОВТОРЕНИЯ'", "Должны быть положительные числа")
        except:
            messagebox.showerror("Ошибка при вводе 'ПОВТОРЕНИЯ'", "Должны быть числа")

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

    def general_diagram_period(self, x=[], period=[], y=[]):
        """
        Выводим диаграмму, построенную на данных из указанного периода. При этом если ранне указана сортировка по
        упражнения, то диаграмма это учтет.
        :param x:
        :param period:
        :param y:
        :return:
        """
        data = load_data()
        try:
            dt1 = datetime.strptime(self.beginning_period_value.get(), '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime(self.end_period_value.get(), '%Y-%m-%d %H:%M:%S')
        except:
            dt1 = datetime.strptime('2020-10-28 00:00:00', '%Y-%m-%d %H:%M:%S')
            dt2 = datetime.strptime('2024-12-30 00:00:00', '%Y-%m-%d %H:%M:%S')
        for entry in data:
            if self.value_inside.get() == 'Без сортировки':
                dt3 = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                if dt3 > dt1 and dt3 < dt2:
                    self.tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'],
                                                         entry['repetitions']))
                    x.append(entry['exercise'])
                    y.append(int(entry['weight']) * int(entry['repetitions']))
                    period.append(entry['date'])
            else:
                if entry['exercise'] == self.value_inside.get():
                    dt3 = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                    if dt3 > dt1 and dt3 < dt2:
                        self.tree.insert('', tk.END, values=(entry['date'], entry['exercise'],
                                                             entry['weight'], entry['repetitions']))
                        x.append(entry['date'])
                        y.append(int(entry['weight']) * int(entry['repetitions']))
                        period.append(entry['date'])
        self.tree.grid(row=0, column=0)
        if self.value_inside.get() == 'Без сортировки':
            plt.figure(figsize=(10, 6))
            plt.bar(x, y)
            plt.xlabel(f'Период от {min(period)} до {max(period)}')
            plt.ylabel('Суммарная масса поднятого веса, кг')
            plt.title('Диаграмма суммы поднятого веса')
            vertical_labels = ['\n'.join(wrap(label, 200)) for label in x]
            # Добавляем подписи оси x вертикальными словами
            plt.xticks(x, vertical_labels, rotation=90)
            plt.tight_layout()
            plt.show()
        else:
            plt.figure(figsize=(10, 6))
            plt.bar(x, y)
            plt.xlabel(f'Период от {min(period)} до {max(period)}')
            plt.ylabel('Суммарная масса поднятого веса, кг')
            plt.title(f'Диаграмма суммы поднятого веса при упражнении "{self.value_inside.get()}"')
            vertical_labels = ['\n'.join(wrap(label, 200)) for label in x]
            # Добавляем подписи оси x вертикальными словами
            plt.xticks(x, vertical_labels, rotation=90)
            plt.tight_layout()
            plt.show()

    def general_diagram(self, x=[], y=[], period=[]):
        """
        Выводим диаграмму, построенную на данных из training_log.json файла. При этом если ранне указана сортировка по
        упражнения, то диаграмма это учтет.
        :param x:
        :param y:
        :param period:
        :return:
        """
        for entry in self.data:
            if self.value_inside.get() == 'Без сортировки':
                self.tree.insert('', tk.END,
                                 values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
                x.append(entry['exercise'])
                y.append(int(entry['weight']) * int(entry['repetitions']))
                period.append(entry['date'])
            else:
                if entry['exercise'] == self.value_inside.get():
                    x.append(entry['date'])
                    y.append(int(entry['weight']) * int(entry['repetitions']))
                    period.append(entry['date'])
                    self.tree.insert('', tk.END,
                                     values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        self.tree.grid(row=0, column=0)
        if self.value_inside.get() == 'Без сортировки':
            plt.figure(figsize=(10, 6))
            plt.bar(x, y)
            plt.xlabel(f'Период от {min(period)} до {max(period)}')
            plt.ylabel('Суммарная масса поднятого веса, кг')
            plt.title('Диаграмма суммы поднятого веса')
            vertical_labels = ['\n'.join(wrap(label, 200)) for label in x]
            # Добавляем подписи оси x вертикальными словами
            plt.xticks(x, vertical_labels, rotation=90)
            plt.tight_layout()
            plt.show()
        else:
            plt.figure(figsize=(10, 6))
            plt.bar(x, y)
            plt.xlabel(f'Период от {min(period)} до {max(period)}')
            plt.ylabel('Суммарная масса поднятого веса, кг')
            plt.title(f'Диаграмма суммы поднятого веса при упражнении "{self.value_inside.get()}"')
            vertical_labels = ['\n'.join(wrap(label, 200)) for label in x]
            # Добавляем подписи оси x вертикальными словами
            plt.xticks(x, vertical_labels, rotation=90)
            plt.tight_layout()
            plt.show()

    def view_records(self):
        """
        Метод выводит все сохраненные значения из training_log.json файла.
        :return:
        """
        self.data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")
        self.tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")
        for entry in self.data:
            if self.value_inside.get() == 'Без сортировки':
                self.tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
            else:
                if entry['exercise'] == self.value_inside.get():
                    self.tree.insert('', tk.END,
                                values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))
        self.tree.grid(row=0, column=0)
        # Создает боковую прокрутку таблицы по вертикали
        game_scroll = Scrollbar(records_window)
        current_columns = game_scroll.grid_size()[0]
        game_scroll.grid(row=0, column=current_columns + 1, sticky="ns")
        # Создает виджеты которыми можно управлять данными таблицы
        self.playerdate = Label(records_window, text="Дата")
        self.playerdate.grid(row=1, column=0, sticky=tk.W, padx=45, pady=5)
        self.playerdate_entry = Entry(records_window)
        self.playerdate_entry.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.playerexercise = Label(records_window, text="Упражнение")
        self.playerexercise.grid(row=1, column=0, sticky=tk.W, padx=160)
        self.playerexercise_entry = Entry(records_window)
        self.playerexercise_entry.grid(row=2, column=0, sticky=tk.W, padx=120)
        self.playerweight = Label(records_window, text="Вес")
        self.playerweight.grid(row=1, column=0, sticky=tk.W, padx=280)
        self.playerweight_entry = Entry(records_window)
        self.playerweight_entry.grid(row=2, column=0, sticky=tk.W, padx=240)
        self.playerrepetitions = Label(records_window, text="Повторения")
        self.playerrepetitions.grid(row=1, column=0, sticky=tk.W, padx=400)
        self.playerrepetitions_entry = Entry(records_window)
        self.playerrepetitions_entry.grid(row=2, column=0, sticky=tk.W, padx=360)
        self.select_button = Button(records_window, text="Выбрать строку", command=self.select_record)
        self.select_button.grid(row=3, column=0, sticky=tk.W, padx=5)
        self.edit_button = Button(records_window, text="Сохранить изменения", command=self.update_record)
        self.edit_button.grid(row=3, column=0, sticky=tk.W, padx=115)
        self.edit_button = Button(records_window, text="Удалить запись", command=self.delite_record)
        self.edit_button.grid(row=3, column=0, sticky=tk.W, padx=260)
        self.gen_diagram = Button(records_window, text="Диаграмма", command=self.general_diagram)
        self.gen_diagram.grid(row=3, column=0, sticky=tk.W, padx=370)

    def importing_csv_file(self):
        """
        Импортирует данные из файлов формата .csv При этом проверки файла нет. Изменяет данные в training_log.json файле
        :return:
        """
        file_path = filedialog.askopenfilename(
            title="Выберите файл для импорта",
            filetypes=[('All Files', '*.*'), ("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        # Чтение CSV-файла
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
        # Список для хранения данных
            data = list(reader)
        json_data = []
        # Заполняем словарь данными из CSV
        for row in data[1:]:  # Пропускаем заголовок
            json_data.append(row)
        # Запись данных в JSON-файл
        with open('training_log.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    def save_csv_file(self):
        """
        Передает данные из training_log.json в файл формата .csv, при этом сохраняет его в необходимое вам место.
        :return:
        """
        filename = filedialog.asksaveasfilename(filetypes=[('CSV', '*.csv')])
        with open('training_log.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        # Открытие файла для записи CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            # Запись заголовков
            writer.writeheader()
            # Запись данных
            for item in data:
                writer.writerow(item)
        messagebox.showinfo("Успешно", f"Создан файл - {filename}")

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
