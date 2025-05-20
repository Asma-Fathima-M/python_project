import cx_Oracle
from app import get_db

try:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    print("Success! Found courses:", cursor.fetchall())
    conn.close()
except Exception as e:
    print("Connection failed:", e)