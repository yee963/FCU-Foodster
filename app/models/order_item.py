from app.models.database import get_db_connection

class OrderItem:
    @staticmethod
    def create(data):
        """
        新增一筆訂單明細記錄
        :param data: dict, 包含 order_id, item_name, price, quantity
        :return: int, 新增的明細 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO order_items (order_id, item_name, price, quantity)
                VALUES (?, ?, ?, ?)
                """,
                (
                    data.get('order_id'),
                    data.get('item_name'),
                    data.get('price'),
                    data.get('quantity', 1)
                )
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            print(f"Error creating order item: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有訂單明細
        :return: list of dicts
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_items")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching order items: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(item_id):
        """
        取得單筆明細
        :param item_id: int
        :return: dict or None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching order item {item_id}: {e}")
            return None
        finally:
            conn.close()
            
    @staticmethod
    def get_by_order_id(order_id):
        """
        取得單張訂單底下的所有明細
        :param order_id: int
        :return: list of dicts
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching items for order {order_id}: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(item_id, data):
        """
        更新明細記錄
        :param item_id: int
        :param data: dict, 欲更新的欄位與值
        :return: bool, 是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            fields = []
            values = []
            for key, value in data.items():
                fields.append(f"{key} = ?")
                values.append(value)
            
            if not fields:
                return False
                
            values.append(item_id)
            query = f"UPDATE order_items SET {', '.join(fields)} WHERE id = ?"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating order item {item_id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(item_id):
        """
        刪除明細記錄
        :param item_id: int
        :return: bool, 是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting order item {item_id}: {e}")
            return False
        finally:
            conn.close()
