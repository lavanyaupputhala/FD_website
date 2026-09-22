import sqlite3

connection = sqlite3.connect("decorations.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS decorations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    image TEXT NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")