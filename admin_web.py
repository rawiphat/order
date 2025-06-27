
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, username, order_text, status FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    conn.close()
    return render_template("index.html", orders=orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
