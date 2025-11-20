import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.json"

def load_users():
    """Загружает всех пользователей из JSON."""
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    """Сохраняет словарь пользователей в JSON."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def register_user(username, password):
    """Регистрирует пользователя. Возвращает True или False."""
    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": generate_password_hash(password)
    }

    save_users(users)
    return True


def validate_user(username, password):
    """Проверяет логин/пароль пользователя."""
    users = load_users()

    if username not in users:
        return False

    return check_password_hash(users[username]["password"], password)
