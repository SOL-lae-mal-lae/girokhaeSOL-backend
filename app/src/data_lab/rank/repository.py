# from app.database.core import get_connection

# def test_repository():
#     conn = get_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT NOW() as now_time;")
#             result = cursor.fetchone()
#             return result
#     finally:
#         conn.close()
