import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime, timedelta
import os
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Улучшенный Expense Tracker")
        self.root.geometry("800x600")

        # Данные
        self.expenses = []
        self.filtered_expenses = []

        # Загрузка данных
        self.load_data()

        # Создание интерфейса
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавить расход", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Поля ввода
        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Категория:").grid(row=1, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", "Одежда", "Образование", "Другое"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var,
                                       values=categories, state="readonly")
        self.category_combo.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Дата:").grid(row=2, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Описание:").grid(row=3, column=0, sticky=tk.W)
        self.description_entry = ttk.Entry(input_frame, width=30)
        self.description_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить расход",
                  command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)

        # Фрейм для фильтрации и статистики
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация и статистика", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Фильтрация по категории
        ttk.Label(filter_frame, text="Фильтр категории:").grid(row=0, column=0, sticky=tk.W)
        self.filter_category_var = tk.StringVar(value="Все")
        filter_categories = ["Все"] + categories
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                                  values=filter_categories, state="readonly", width=15)
        self.filter_combo.grid(row=0, column=1, padx=5, pady=2)

        # Фильтрация по периоду
        ttk.Label(filter_frame, text="Период:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.period_var = tk.StringVar(value="За всё время")
        periods = ["За всё время", "Сегодня", "Эта неделя", "Этот месяц", "Этот год"]
        self.period_combo = ttk.Combobox(filter_frame, textvariable=self.period_var,
                      values=periods, state="readonly", width=15)
        self.period_combo.grid(row=0, column=3, padx=5, pady=2)

        # Кнопки фильтрации
        ttk.Button(filter_frame, text="Применить фильтры",
                  command=self.apply_filters).grid(row=0, column=4, padx=10)
        ttk.Button(filter_frame, text="Сбросить фильтры",
                  command=self.reset_filters).grid(row=0, column=5)

        # Статистика
        self.stats_label = ttk.Label(filter_frame, text="Общая сумма: 0 руб.")
        self.stats_label.grid(row=1, column=0, columnspan=6, pady=5)

        # Таблица
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        columns = ("ID", "Сумма", "Категория", "Дата", "Описание")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(button_frame, text="Удалить выбранный",
                  command=self.delete_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Экспорт в JSON",
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Импорт из JSON",
                  command=self.import_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить все",
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    def validate_input(self):
        """Проверка корректности ввода данных"""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат суммы")
            return False

        category = self.category_var.get()
        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию")
            return False

        date_str = self.date
