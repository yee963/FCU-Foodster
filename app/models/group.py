from app.models.database import get_db_connection

class Group:
    @staticmethod
    def create(data):
        """
        新增一筆揪團記錄
        :param data: dict, 包含 creator_id, store_id, delivery_fee, pickup_location, deadline, status
        :return: int, 新增的揪團 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO groups (creator_id, store_id, delivery_fee, pickup_location, deadline, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get('creator_id'),
                    data.get('store_id'),
                    data.get('delivery_fee', 0),
                    data.get('pickup_location'),
                    data.get('deadline'),
                    data.get('status', 'open')
                )
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            print(f"Error creating group: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有揪團記錄 (包含店家名稱與發起人名稱)
        :return: list of dicts
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT groups.*, stores.name AS store_name, users.username AS creator_name
                FROM groups
                LEFT JOIN stores ON groups.store_id = stores.id
                LEFT JOIN users ON groups.creator_id = users.id
                ORDER BY groups.created_at DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching groups: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(group_id):
        """
        取得單筆揪團記錄 (包含店家名稱與發起人名稱)
        :param group_id: int
        :return: dict or None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT groups.*, stores.name AS store_name, users.username AS creator_name
                FROM groups
                LEFT JOIN stores ON groups.store_id = stores.id
                LEFT JOIN users ON groups.creator_id = users.id
                WHERE groups.id = ?
            """, (group_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching group {group_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(group_id, data):
        """
        更新揪團記錄
        :param group_id: int
        :param data: dict, 欲更新的欄位與值
        :return: bool, 是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 動態組裝 SET 語法
            fields = []
            values = []
            for key, value in data.items():
                fields.append(f"{key} = ?")
                values.append(value)
            
            if not fields:
                return False
                
            values.append(group_id)
            query = f"UPDATE groups SET {', '.join(fields)} WHERE id = ?"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating group {group_id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(group_id):
        """
        刪除揪團記錄
        :param group_id: int
        :return: bool, 是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting group {group_id}: {e}")
            return False
        finally:
            conn.close()
