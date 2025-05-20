import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        dsn = cx_Oracle.makedsn(
            os.getenv("DB_HOST"), 
            1521, 
            service_name=os.getenv("DB_SERVICE")
        )
        return cx_Oracle.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            dsn=dsn
        )
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        raise