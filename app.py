from flask import Flask, send_file
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "barcodes.db")
BARCODES_FOLDER = os.path.join(BASE_DIR, "barcodes")  

SUCCESS_IMG = os.path.join(BASE_DIR, "success.jpg")
USED_IMG = os.path.join(BASE_DIR, "used.jpg")

@app.route('/scan/<uuid>')
def scan(uuid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT used FROM barcodes WHERE uuid=?", (uuid,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return "باركود غير موجود", 404

    elif row[0]:  # إذا الباركود مستخدم قبل
        conn.close()
        return send_file(USED_IMG, mimetype='image/jpeg')

    else:  # أول مرة يُستخدم
        cursor.execute("UPDATE barcodes SET used=1 WHERE uuid=?", (uuid,))
        conn.commit()
        conn.close()
        return send_file(SUCCESS_IMG, mimetype='image/jpeg')

@app.route('/barcode/<uuid>')
def get_barcode(uuid):
    file_path = os.path.join(BARCODES_FOLDER, f"{uuid}.png")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        return "باركود غير موجود", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
