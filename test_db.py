# EduTrack/test_db.py
import cx_Oracle

def test_connection():
    try:
        conn = cx_Oracle.connect("system/new_password@localhost:1521/XE")
        cursor = conn.cursor()
        
        # Test courses table
        cursor.execute("SELECT * FROM courses")
        print("Courses:", cursor.fetchall())
        
        # Test trigger by inserting new course
        cursor.execute("""
            INSERT INTO courses (course_name, description, credit_hours)
            VALUES ('Python Programming', 'Learn Python basics', 3)
        """)
        conn.commit()
        
        print("Connection successful! New course added.")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)

test_connection()