from app.models.database import get_db_connection

class Order:
    @staticmethod
    def create(data):
        """
        新增一筆訂單記錄
        :param data: dict, 包含 group_id, user_id, items_total, split_fee, final_amount, payment_status
        :return: int, 新增的訂單 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO orders (group_id, user_id, items_total, split_fee, final_amount, payment_status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get('group_id'),
                    data.get('user_id'),
                    data.get('items_total', 0),
                    data.get('split_fee', 0),
                    data.get('final_amount', 0),
                    data.get('payment_status', 'unpaid')
                )
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            print(f"Error creating order: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有訂單記錄
        :return: list of dicts
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(order_id):
        """
        取得單筆訂單記錄
        :param order_id: int
        :return: dict or None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching order {order_id}: {e}")
            return None
        finally:
            conn.close()
            
    @staticmethod
    def get_by_group_id(group_id):
        """
        取得某個揪團下的所有訂單
        :param group_id: int
        :return: list of dicts
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE group_id = ?", (group_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching orders for group {group_id}: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(order_id, data):
        """
        更新訂單記錄
        :param order_id: int
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
                
            values.append(order_id)
            query = f"UPDATE orders SET {', '.join(fields)} WHERE id = ?"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating order {order_id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(order_id):
        """
        刪除訂單記錄
        :param order_id: int
        :return: bool, 是否成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting order {order_id}: {e}")
            return False
        finally:
            conn.close()
