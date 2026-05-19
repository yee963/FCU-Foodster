import sqlite3
import os

DATABASE_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    """?–å???SQLite è³‡æ?åº«ç????"""
    # ç¢ºä? instance ?®é?å­˜åœ¨
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    # è®“æŸ¥è©¢ç??œå¯ä»¥å?å­—å…¸ä¸€æ¨?€é?æ¬„ä??ç¨±å­˜å?
    conn.row_factory = sqlite3.Row
    return conn
