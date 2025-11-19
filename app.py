from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import pandas as pd
from werkzeug.utils import secure_filename
from users import USERS
import importlib


app = Flask(__name__)
app.secret_key = "secret-key-change-me"

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# импортируем пользователей и их пароли из файла
try:
    from users import USERS
except ImportError:
    raise Exception(
        "Файл users.py не найден. Скопируйте users_example.py → users.py и добавьте пользователей."
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in USERS and USERS[email]["password"] == password:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Неверный логин или пароль")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# ---------------------------------------
#             СТРАНИЦЫ
# ---------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    email = session["user"]                   # email пользователя
    user_data = USERS[email]                 # словарь данных пользователя
    password_hidden = "*" * len(user_data["password"])  # скрытый пароль

    return render_template(
        "dashboard.html",
        email=email,
        password_hidden=password_hidden,
        templates=user_data.get("template", [])
    )
    
@app.route("/convert/<template_id>", methods=["GET", "POST"])
def convert_template(template_id):
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["file"]

        if not file:
            return render_template(
                "convert_template.html",
                template_id=template_id,
                error="Выберите файл"
            )

        filename = secure_filename(file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        try:
            # Загружаем обработчик по имени
            module = importlib.import_module(f"processors.process_{template_id}")

            # Выполняем обработку
            df = module.process(upload_path)

        except ModuleNotFoundError:
            return render_template(
                "convert_template.html",
                template_id=template_id,
                error=f"Шаблон process_{template_id}.py не найден"
            )
        except Exception as e:
            return render_template(
                "convert_template.html",
                template_id=template_id,
                error=f"Ошибка обработки: {e}"
            )

        # Сохраняем результат
        output_filename = f"converted_{filename}"
        output_path = os.path.join(CONVERTED_FOLDER, output_filename)
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template("convert_template.html", template_id=template_id)


@app.route("/add_template")
def add_template():
    return "<h2>Здесь будет добавление нового шаблона</h2>"



if __name__ == "__main__":
    app.run(debug=True)
