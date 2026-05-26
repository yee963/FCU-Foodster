import sqlite3
import os

DATABASE_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫並塞入種子資料"""
    db_exists = os.path.exists(DATABASE_PATH)
    
    # 確保資料夾存在
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if not db_exists:
        print("Initializing database...")
        # 讀取並執行 schema.sql
        schema_path = os.path.join('database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)
            conn.commit()
            
            # 塞入種子資料 (預設使用者)
            users_data = [
                (1, '王棕葆', 'zbwang@fcu.edu.tw'),
                (2, '余芃燊', 'fsyu@fcu.edu.tw'),
                (3, '賴俊杰', 'jjlai@fcu.edu.tw')
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO users (id, username, email) VALUES (?, ?, ?)",
                users_data
            )
            
            # 塞入種子資料 (預設店家)
            stores_data = [
                (1, '逢甲燒肉飯', '台中市西屯區文華路 100 號'),
                (2, '校園麥當勞', '台中市西屯區福星路 427 號'),
                (3, '大苑子逢甲店', '台中市西屯區文華路 55 號')
            ]
            cursor.executemany(
                "INSERT OR IGNORE INTO stores (id, name, address) VALUES (?, ?, ?)",
                stores_data
            )
            
            conn.commit()
            print("Database initialized successfully with seed data.")
        else:
            print(f"Error: Schema file not found at {schema_path}")
    
    conn.close()
