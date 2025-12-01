from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
app = Flask(__name__)
app.config["DATABASE"] = DB_PATH

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript("""
        CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE
        );
        """)
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    db = get_db()
    warehouses = db.execute("SELECT * FROM warehouses").fetchall()
    return render_template("index.html", warehouses=warehouses)

@app.route("/warehouse/<int:w_id>")
def warehouse_view(w_id):
    db = get_db()
    warehouse = db.execute("SELECT * FROM warehouses WHERE id = ?", (w_id,)).fetchone()
    products = db.execute("SELECT * FROM products WHERE warehouse_id = ?", (w_id,)).fetchall()
    return render_template("warehouse.html", warehouse=warehouse, products=products)

@app.route("/warehouse/add", methods=["POST"])
def warehouse_add():
    name = request.form.get("name", "").strip()
    if name:
        db = get_db()
        db.execute("INSERT INTO warehouses (name) VALUES (?)", (name,))
        db.commit()
    return redirect(url_for("index"))

@app.route("/product/add/<int:w_id>", methods=["POST"])
def product_add(w_id):
    name = request.form.get("name", "").strip()
    try:
        qty = int(request.form.get("quantity", "0") or 0)
    except ValueError:
        qty = 0
    if name:
        db = get_db()
        db.execute("INSERT INTO products (warehouse_id, name, quantity) VALUES (?, ?, ?)", (w_id, name, qty))
        db.commit()
    return redirect(url_for("warehouse_view", w_id=w_id))

@app.route("/product/delete/<int:p_id>", methods=["POST"])
def product_delete(p_id):
    db = get_db()
    row = db.execute("SELECT warehouse_id FROM products WHERE id = ?", (p_id,)).fetchone()
    if row:
        w_id = row["warehouse_id"]
        db.execute("DELETE FROM products WHERE id = ?", (p_id,))
        db.commit()
        return redirect(url_for("warehouse_view", w_id=w_id))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
