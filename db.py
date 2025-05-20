import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

class OracleDB:
    @staticmethod
    def get_connection():
        try:
            return cx_Oracle.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                dsn=cx_Oracle.makedsn(
                    os.getenv("DB_HOST"),
                    int(os.getenv("DB_PORT", "1521")),
                    service_name=os.getenv("DB_SERVICE", "XE")
                )
            )
        except cx_Oracle.DatabaseError as e:
            print(f"Database connection failed: {e}")
            raise