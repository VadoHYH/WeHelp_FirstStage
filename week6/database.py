import mysql.connector

# 建立 MySQL 連線資訊
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "vadomysql",  # 你的 MySQL 密碼
    "database": "website"  # 資料庫名稱
}

# 建立資料庫連線
def get_db():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 讓查詢結果以字典方式回傳
    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()
