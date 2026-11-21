import sqlite3
import tkinter as tk
from tkinter import messagebox

def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ('admin',   'admin',   'admin123',   'Имя Пользователя'),
            ('manager', 'manager', 'manager123', 'Имя Пользователя'),
            ('user',    'user',    'user123',    'Имя Пользователя'),
        ]
        cursor.executemany(
            "INSERT INTO users (role, login, password, name) VALUES (?, ?, ?, ?)",
            users
        )
    
    conn.commit()
    conn.close()

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("350x230")
        self.root.resizable(False, False)
        
        tk.Label(root, text="Логин:").pack(pady=(15, 0))
        self.entry_login = tk.Entry(root, width=30)
        self.entry_login.pack(pady=5)
        
        tk.Label(root, text="Пароль:").pack()
        self.entry_password = tk.Entry(root, width=30, show="*")
        self.entry_password.pack(pady=5)
        
        tk.Button(root, text="Войти", width=20, command=self.login).pack(pady=8)
        tk.Button(root, text="Войти как гость", width=20, command=self.login_guest).pack()
        
        self.entry_password.bind('<Return>', lambda e: self.login())
    
    def login(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()
        
        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return
        
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, name FROM users WHERE login=? AND password=?",
            (login, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            role, name = user
            self.open_feed(f"Добро пожаловать, {name}!\nВаша роль: {role}")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def login_guest(self):
        self.open_feed("Добро пожаловать, Гость!")
    
    def open_feed(self, greeting):
        self.root.destroy() 
        
        feed = tk.Tk()
        feed.title("Магазин")
        feed.geometry("500x400")
        
        tk.Label(feed, text=greeting, font=("Arial", 12, "bold")).pack(pady=20)
        
        frame = tk.Frame(feed, relief="groove", bd=2)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(frame, text="Тут будет лента товаров",
                 font=("Arial", 14), fg="gray").pack(expand=True)
        
        feed.mainloop()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()