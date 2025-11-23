from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import pandas as pd
from werkzeug.utils import secure_filename
import importlib
from registration import register_user, validate_user, load_users

app = Flask(__name__)
app.secret_key = "secret-key-change-me"

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if validate_user(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Неверный логин или пароль")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    users = load_users()

    user_data = users.get(username)

    if not user_data:
        return "Ошибка: пользователь не найден", 404

    return render_template(
        "dashboard.html",
        email=username,
        password_hidden="********",
        templates=user_data.get("templates", [])
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
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if register_user(username, password):
            session["username"] = username

            return redirect(url_for("dashboard"))
        else:
            return render_template("register.html", error="Логин уже существует")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
