import sqlite3
from pathlib import Path
from modules.db import DATABASE_PATH  # Importamos DATABASE_PATH de db.py

# Verificar que la base de datos existe
db_file = Path(DATABASE_PATH)
if not db_file.exists():
    print(f"❌ No se encontró la base de datos en: {db_file}")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE inspecciones ADD COLUMN categoria TEXT DEFAULT 'Excluido';")
    print("✅ Columna 'categoria' agregada correctamente.")
except sqlite3.OperationalError as e:
    print("⚠️ Atención:", e)

conn.commit()
conn.close()
