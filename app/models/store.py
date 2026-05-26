from app.models.database import get_db_connection

class Store:
    @staticmethod
    def get_all():
        """
        取得所有店家列表
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stores ORDER BY name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching stores: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(store_id):
        """
        取得單筆店家資訊
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stores WHERE id = ?", (store_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching store {store_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_menu(store_id):
        """
        根據店家 ID 取得其菜單品項
        """
        # 靜態模擬菜單，之後若有菜單資料表可改為查詢資料庫
        menus = {
            1: [
                {'name': '招牌烤肉飯', 'price': 90, 'description': '特製醬汁烤肉片，搭配當季配菜'},
                {'name': '香酥雞排飯', 'price': 95, 'description': '現炸大雞排，外酥內嫩'},
                {'name': '特級雙拼飯', 'price': 120, 'description': '烤肉與雞排雙重享受'},
                {'name': '燙青菜', 'price': 30, 'description': '淋上肉燥的高麗菜'}
            ],
            2: [
                {'name': '大麥克套餐', 'price': 140, 'description': '雙層牛肉吉事堡，搭配薯條與可樂'},
                {'name': '麥香魚套餐', 'price': 120, 'description': '經典麥香魚，搭配薯條與可樂'},
                {'name': '麥克雞塊六塊', 'price': 100, 'description': '金黃酥脆麥克雞塊'},
                {'name': '薯條(大)', 'price': 60, 'description': '經典美味金黃薯條'}
            ],
            3: [
                {'name': '鮮榨柳橙綠', 'price': 65, 'description': '新鮮柳橙汁搭配優質綠茶'},
                {'name': '芭樂檸檬', 'price': 60, 'description': '清爽芭樂加上微酸檸檬'},
                {'name': '珍珠奶茶', 'price': 50, 'description': 'Q彈珍珠與濃郁奶茶'},
                {'name': '翡翠檸檬', 'price': 55, 'description': '清香檸檬搭配綠茶'}
            ]
        }
        return menus.get(store_id, [{'name': '預設特餐', 'price': 80, 'description': '店家特製美味餐點'}])
