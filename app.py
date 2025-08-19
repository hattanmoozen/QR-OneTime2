from flask import Flask, send_file
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "barcodes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS barcodes (
                    code TEXT PRIMARY KEY,
                    used INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

@app.route('/scan/<code>')
def scan(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT used FROM barcodes WHERE code=?", (code,))
    row = c.fetchone()

    if row is None:
        # الكود غير موجود
        conn.close()
        return "❌ الكود غير صالح"

    if row[0] == 0:
        # أول مرة
        c.execute("UPDATE barcodes SET used=1 WHERE code=?", (code,))
        conn.commit()
        conn.close()
        return send_file("success.jpg", mimetype="image/jpeg")
    else:
        # تم استخدامه من قبل
        conn.close()
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/verify/<code>")
def verify(code):
    conn = sqlite3.connect(os.path.join(BASE_DIR, "barcodes.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT used FROM barcodes WHERE code = ?", (code,))
    row = cursor.fetchone()
    if row and row[0] == 0:
        cursor.execute("UPDATE barcodes SET used = 1 WHERE code = ?", (code,))
        conn.commit()
        conn.close()
        return send_file(os.path.join(BASE_DIR, "success.jpg"), mimetype="image/jpeg")
    else:
        conn.close()
        return send_file(os.path.join(BASE_DIR, "used.jpg"), mimetype="image/jpeg")

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
