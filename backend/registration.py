import json
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .env_utils import load_env


load_env()
USERS_FILE = os.getenv("USERS_FILE")


def is_valid_email(value: str) -> bool:
    """проверка, что логин похож на email."""
    if not value or not isinstance(value, str):
        return False

    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value) is not None


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
    """Регистрирует пользователя. вернет True или False."""
    if not is_valid_email(username):
        return False

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
