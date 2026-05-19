from flask import render_template, request, redirect, url_for, flash
from . import order_bp
from app.models.group import Group
from app.models.order import Order
from app.models.order_item import OrderItem

@order_bp.route('/groups/<int:group_id>/orders/new', methods=['GET'])
def new_order(group_id):
    """
    顯示參團點餐表單
    """
    group = Group.get_by_id(group_id)
    if not group or group['status'] != 'open':
        return "Cannot join this group", 400
    return "New Order Form Placeholder", 200

@order_bp.route('/groups/<int:group_id>/orders', methods=['POST'])
def create_order(group_id):
    """
    送出點餐
    """
    group = Group.get_by_id(group_id)
    if not group or group['status'] != 'open':
        flash("該揪團已經關閉，無法點餐")
        return redirect(url_for('group.detail', id=group_id))
        
    # 假設前端傳入的方式為：
    # item_name_1, price_1, quantity_1
    # item_name_2, price_2, quantity_2
    
    user_id = request.form.get('user_id', 2) # 預設 user 2
    
    # 解析表單中的餐點
    items = []
    items_total = 0
    
    for key in request.form.keys():
        if key.startswith('item_name_'):
            idx = key.split('_')[2]
            name = request.form.get(key)
            price = int(request.form.get(f"price_{idx}", 0))
            quantity = int(request.form.get(f"quantity_{idx}", 1))
            
            if name and price > 0:
                items.append({
                    'item_name': name,
                    'price': price,
                    'quantity': quantity
                })
                items_total += price * quantity
                
    if not items:
        flash("請至少點一項餐點")
        return redirect(url_for('order.new_order', group_id=group_id))
        
    # 建立 Order 主檔
    order_id = Order.create({
        'group_id': group_id,
        'user_id': user_id,
        'items_total': items_total,
        'split_fee': 0, # 等結單才算
        'final_amount': items_total, # 暫時先等於餐費
        'payment_status': 'unpaid'
    })
    
    # 建立 OrderItem 明細
    for item in items:
        item['order_id'] = order_id
        OrderItem.create(item)
        
    flash("成功加入揪團！")
    return redirect(url_for('group.detail', id=group_id))

@order_bp.route('/orders/<int:id>/pay', methods=['POST'])
def pay_order(id):
    """
    更新付款狀態
    """
    order = Order.get_by_id(id)
    if not order:
        return "Order not found", 404
        
    Order.update(id, {'payment_status': 'paid'})
    flash("已標記為付款完成！")
    
    return redirect(url_for('group.detail', id=order['group_id']))
