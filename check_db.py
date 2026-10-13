import sqlite3

conn = sqlite3.connect('conferences.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

users = cursor.execute("SELECT id, login, password FROM users").fetchall()

print(f"{'ID':<5} {'LOGIN':<15} {'PASSWORD (хеш)':<40}")
print("-" * 65)
for user in users:
    print(f"{user['id']:<5} {user['login']:<15} {user['password']:<40}")

conn.close()