from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Product data
products = [
    {"id": 1, "name": "Phone", "price": 15000, "image": "phone.jpg"},
    {"id": 2, "name": "Laptop", "price": 50000, "image": "laptop.jpg"}
]

@app.route("/")
def home():
    return render_template("home.html", products=products)

@app.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):
    if "cart" not in session:
        session["cart"] = []

    for p in products:
        if p["id"] == pid:
            session["cart"].append(p)

    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = 0

    for item in cart_items:
        total += int(item["price"])

    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            return "Email already registered"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("home"))
        else:
            return "Invalid login details"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
