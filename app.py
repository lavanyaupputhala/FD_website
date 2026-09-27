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


@app.route("/add-decoration", methods=["GET", "POST"])
def add_decoration():
    if request.method == "GET":
        return render_template("add_decoration.html")

    category = request.form["category"]
    images = request.files.getlist("images")

    connection = get_db()

    for image in images:

        if image and image.filename:
            image_path = "static/uploads/" + image.filename

            image.save(image_path)

            connection.execute(
                "INSERT INTO decorations (category, image) VALUES (?, ?)",
                (category, image.filename)
            )

    connection.commit()
    connection.close()

    return "Decorations added successfully!"


@app.route("/edit-decoration")
def edit_decoration():
    connection = get_db()

    decorations = connection.execute(
        "SELECT * FROM decorations"
    ).fetchall()

    connection.close()

    return render_template(
        "edit_decoration.html",
        decorations=decorations
    )


@app.route("/edit-decoration/<int:id>", methods=["GET", "POST"])
def edit_one_decoration(id):
    connection = get_db()

    if request.method == "POST":
        category = request.form["category"]

        connection.execute(
            "UPDATE decorations SET category = ? WHERE id = ?",
            (category, id)
        )

        connection.commit()
        connection.close()

        return "Decoration updated successfully!"

    decoration = connection.execute(
        "SELECT * FROM decorations WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        "edit_one_decoration.html",
        decoration=decoration
    )


@app.route("/delete-decoration", methods=["GET", "POST"])
def delete_decoration():
    connection = get_db()

    if request.method == "POST":
        decoration_id = request.form["decoration_id"]

        connection.execute(
            "DELETE FROM decorations WHERE id = ?",
            (decoration_id,)
        )

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


@app.route("/delete-decoration/<int:id>")
def delete_one_decoration(id):
    connection = get_db()

    decoration = connection.execute(
        "SELECT * FROM decorations WHERE id = ?",
        (id,)
    ).fetchone()

    if decoration:
        connection.execute(
            "DELETE FROM decorations WHERE id = ?",
            (id,)
        )

        connection.commit()

    connection.close()

    return "Decoration deleted successfully!"


@app.route("/owner-logout")
def owner_logout():
    session.pop("owner_logged_in", None)

    return render_template("owner_login.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )