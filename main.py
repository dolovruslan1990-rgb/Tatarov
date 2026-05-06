import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Количество страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        self.add_button = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.filter_genre = tk.Entry(self.root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Мин. страниц:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.filter_pages = tk.Entry(self.root, width=30)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=2)

        self.apply_filter_button = tk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        self.apply_filter_button.grid(row=7, column=0, pady=5)

        self.reset_filter_button = tk.Button(self.root, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_filter_button.grid(row=7, column=1, pady=5)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # Кнопки сохранения/загрузки
        self.save_button = tk.Button(self.root, text="Сохранить в JSON", command=self.save_data)
        self.save_button.grid(row=9, column=0, pady=5)

        self.load_button = tk.Button(self.root, text="Загрузить из JSON", command=self.load_data)
        self.load_button.grid(row=9, column=1, pady=5)
