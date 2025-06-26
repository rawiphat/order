from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB = "orders.db"

# ✅ สร้างไฟล์ฐานข้อมูลและตาราง orders ถ้ายังไม่มี
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            order_text TEXT,
            status TEXT,
            notified INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# HTML UI
TEMPLATE = '''
<h2>📋 รายการออเดอร์ทั้งหมด</h2>
<table border=1 cellpadding=6>
<tr><th>ID</th><th>User ID</th><th>ข้อความ</th><th>สถานะ</th><th>จัดการ</th></tr>
{% for o in orders %}
<tr>
  <td>{{ o[0] }}</td><td>{{ o[1] }}</td><td>{{ o[2] }}</td><td>{{ o[3] }}</td>
  <td>
    <form method="post" action="/update/{{ o[0] }}" style="display:inline;">
      <button name="action" value="confirm">✅ ยืนยัน</button>
      <button name="action" value="reject">❌ ปฏิเสธ</button>
    </form>
    <form method="post" action="/delete/{{ o[0] }}" style="display:inline;">
      <button>🗑️ ลบ</button>
    </form>
  </td>
</tr>
{% endfor %}
</table>
'''

@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return render_template_string(TEMPLATE, orders=orders)

@app.route("/update/<int:order_id>", methods=["POST"])
def update_order(order_id):
    action = request.form.get("action")
    new_status = "ยืนยันแล้ว" if action == "confirm" else "ถูกปฏิเสธ"
    conn = sqlite3.connect(DB)
    if new_status == "ยืนยันแล้ว":
        conn.execute("UPDATE orders SET status=?, notified=0 WHERE id=?", (new_status, order_id))
    else:
        conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    print("✅ Flask Web Admin พร้อมที่ http://localhost:8080")
    app.run(debug=True, port=8080)