import sqlite3
import os
import zipfile

# إنشاء قاعدة بيانات
conn = sqlite3.connect('barcodes.db')
cursor = conn.cursor()

# إنشاء جدول الباركودات
cursor.execute('''
CREATE TABLE IF NOT EXISTS barcodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    used INTEGER DEFAULT 0
)
''')
conn.commit()

# إضافة الباركودات من مجلد ZIP
zip_path = 'barcodes.zip'  # عدّل حسب اسم ملفك
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file in zip_ref.namelist():
        uuid = os.path.splitext(file)[0]  # اسم الملف بدون الامتداد
        cursor.execute("INSERT OR IGNORE INTO barcodes (uuid) VALUES (?)", (uuid,))

conn.commit()
conn.close()
print("تم إنشاء قاعدة البيانات وإضافة الباركودات ✅")
