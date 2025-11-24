from werkzeug.security import generate_password_hash, check_password_hash
from env_utils import load_env
import json
import os


load_env()
USERS_FILE = os.getenv("USERS_FILE")


def load_users():
    """Загружает всех пользователей из JSON."""
    if not os.path.exists(USERS_FILE):
        save_users({})
        return {}

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
