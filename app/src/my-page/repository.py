import pymysql
from pymysql.cursors import DictCursor
from app.core.config import settings

def insert_test(name: str):
    conn = pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        charset='utf8mb4',
    )
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO test (name) VALUES (%s)"
            cursor.execute(sql, (name,))
        conn.commit()
    finally:
        conn.close()


def get_tests():
    conn = pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        charset='utf8mb4',
        cursorclass=DictCursor,       # ✅ 추가!
    )
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM test"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()
