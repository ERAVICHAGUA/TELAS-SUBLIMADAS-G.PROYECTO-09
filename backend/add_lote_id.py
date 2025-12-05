import sqlite3
from modules.db import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE inspecciones ADD COLUMN lote_id INTEGER;")
    print("✅ Columna 'lote_id' agregada correctamente.")
except sqlite3.OperationalError as e:
    print("⚠️ Atención:", e)

conn.commit()
conn.close()
