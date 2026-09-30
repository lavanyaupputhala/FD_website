from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import os
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "fd_website_secret_key"

app.config["UPLOAD_FOLDER"] = "static/uploads"


def get_db():
    connection = sqlite3.connect("decorations.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/haldi")
def haldi():
    connection = get_db()

    decorations = connection.execute(
        "SELECT * FROM decorations WHERE category = ?",
        ("Haldi",)
    ).fetchall()

    connection.close()

    return render_template(
        "haldi.html",
        decorations=decorations
    )


@app.route("/wedding")
def wedding():
    connection = get_db()

    decorations = connection.execute(
        "SELECT * FROM decorations WHERE category = ?",
        ("Wedding",)
    ).fetchall()

    connection.close()

    return render_template(
        "wedding.html",
        decorations=decorations
    )


@app.route("/birthday")
def birthday():
    connection = get_db()

    decorations = connection.execute(
        "SELECT * FROM decorations WHERE category = ?",
        ("Birthday",)
    ).fetchall()

    connection.close()

    return render_template(
        "birthday.html",
        decorations=decorations
    )
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/add-decoration", methods=["GET", "POST"])
def add_decoration():
    if request.method == "GET":
        return render_template("add_decoration.html")

    category = request.form["category"]
    images = request.files.getlist("images")

    connection = get_db()

    for image in images:

        if image and image.filename:

            upload_result = cloudinary.uploader.upload(
                image,
                folder=f"decorations/{category}"
            )

            image_url = upload_result["secure_url"]

            connection.execute(
                "INSERT INTO decorations (category, image) VALUES (?, ?)",
                (category, image_url)
            )

    connection.commit()
    connection.close()

    return "Decorations added successfully!"
@app.route("/owner-login", methods=["GET", "POST"])
def owner_login():

    if request.method == "GET":
        return render_template("owner_login.html")

    username = request.form["username"]
    password = request.form["password"]

    if username == "owner" and password == "1234":
        session["owner_logged_in"] = True
        return render_template("owner.html")

    return "Invalid username or password!"
@app.route("/owner")
def owner():
    if not session.get("owner_logged_in"):
        return '<h2>Please login first!</h2><a href="/owner-login"><button>Login</button></a>'
    connection = get_db()

    decorations = connection.execute(
        "SELECT * FROM decorations"
    ).fetchall()

    connection.close()

    return render_template(
        "owner.html",
        decorations=decorations
    )


@app.route("/owner-logout")
def owner_logout():
    session.pop("owner_logged_in", None)

    return render_template("owner_login.html")





@app.route("/delete-decoration", methods=["GET", "POST"])
def delete_decoration():
    connection = get_db()

    if request.method == "POST":
        image_path = request.form.get("image_path", "").strip()

        if not image_path:
            connection.close()
            return "No image selected!"

        if image_path.startswith("uploads/"):

            filename = os.path.basename(image_path)

            decoration = connection.execute(
                "SELECT * FROM decorations WHERE image = ?",
                (filename,)
            ).fetchone()

            file_path = os.path.join(
                "static",
                "uploads",
                filename
            )

            if os.path.exists(file_path):
                os.remove(file_path)

            if decoration:
                connection.execute(
                    "DELETE FROM decorations WHERE id = ?",
                    (decoration["id"],)
                )

        elif image_path.startswith("images/"):

            filename = os.path.basename(image_path)

            file_path = os.path.join(
                "static",
                "images",
                filename
            )

            if os.path.exists(file_path):
                os.remove(file_path)

        connection.commit()
        connection.close()

        return "Decoration deleted successfully!"

    decorations = connection.execute(
        "SELECT * FROM decorations"
    ).fetchall()

    connection.close()

    return render_template(
        "delete_decoration.html",
        decorations=decorations
    )
app.run(
    host="0.0.0.0",
    port=5000,
    debug=False
)