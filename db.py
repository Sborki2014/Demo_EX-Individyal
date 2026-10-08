import sqlite3

def init_db():
    conn = sqlite3.connect('conferences.db')
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Таблица заявок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'Новая',
        review TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Создаем админа
    try:
        cursor.execute("INSERT INTO users (login, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)",
                       ('Conf2027', 'Demo77', 'Администратор', '8(999)999-99-99', 'admin@conf.ru'))
    except sqlite3.IntegrityError:
        pass
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("База данных создана.")