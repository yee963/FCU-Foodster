from flask import render_template
from app import app

@app.route('/shop/<int:shop_id>')
def shop_detail(shop_id):
    # Mock data for demonstration
    shop_data = {
        'id': shop_id,
        'name': '逢甲燒肉飯',
        'rating': 4.5,
        'reviews': 128,
        'description': '逢甲大學周邊最熱門的燒肉飯，大份量滿足學生的胃。',
        'menu': [
            {'id': 1, 'name': '招牌烤肉飯', 'price': 90, 'description': '特製醬汁烤肉片，搭配當季配菜'},
            {'id': 2, 'name': '香酥雞排飯', 'price': 95, 'description': '現炸大雞排，外酥內嫩'},
            {'id': 3, 'name': '特級雙拼飯', 'price': 120, 'description': '烤肉與雞排雙重享受'},
            {'id': 4, 'name': '燙青菜', 'price': 30, 'description': '淋上肉燥的高麗菜'}
        ],
        'map_query': '逢甲大學', # Use a generic query for embed API
    }
    
    # Check if a specific shop ID is requested, otherwise return default mock
    if shop_id != 1:
        shop_data['name'] = f'測試店家 {shop_id}'
        shop_data['menu'] = [{'id': 99, 'name': '預設餐點', 'price': 50, 'description': '這是一個測試用店家'}]
        
    return render_template('shop/detail.html', shop=shop_data)
