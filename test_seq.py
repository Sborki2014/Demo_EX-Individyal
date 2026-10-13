from security import hash_password, verify_password

h = hash_password("Demo77")
print(h)
# Пример вывода: $2b$12$abcdefghijklmnopqrstuv

print(verify_password("Demo77", h))   # True
print(verify_password("demo77", h))   # False
print(verify_password("Demo78", h))   # False