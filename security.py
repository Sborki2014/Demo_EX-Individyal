from passlib.context import CryptContext

# Контекст — это "настройка" хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Превращает пароль в хеш.
    
    Пример:
        >>> hash_password("Demo77")
        '$2b$12$K8xPq3...'
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введённый пароль сохранённому хешу.
    Возвращает True, если пароль верный.
    
    Пример:
        >>> verify_password("Demo77", "$2b$12$K8xPq3...")
        True
        >>> verify_password("Wrong", "$2b$12$K8xPq3...")
        False
    """
    return pwd_context.verify(plain_password, hashed_password)