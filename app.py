from flask import Flask, request, send_file
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'barcodes.db'
BARCODES_FOLDER = 'barcodes'  # مجلد الصور بعد فك ZIP

@app.route('/scan/<uuid>')
def scan(uuid):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT used FROM barcodes WHERE uuid=?", (uuid,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return "باركود غير موجود", 404
    elif row[0]:
        conn.close()
        return "الباركود غير صالح", 400
    else:
        cursor.execute("UPDATE barcodes SET used=1 WHERE uuid=?", (uuid,))
        conn.commit()
        conn.close()
        return "تم المسح بنجاح ✅"

@app.route('/barcode/<uuid>')
def get_barcode(uuid):
    file_path = os.path.join(BARCODES_FOLDER, f"{uuid}.png")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        return "باركود غير موجود", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
