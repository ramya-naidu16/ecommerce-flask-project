import sqlite3

db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT,
    password TEXT
)
""")

db.commit()
db.close()

print("Database created successfully")
