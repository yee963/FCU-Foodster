import math
from flask import render_template, request, redirect, url_for, flash
from . import group_bp
from app.models.group import Group
from app.models.order import Order

@group_bp.route('/groups', methods=['GET'])
def index():
    """
    顯示所有開放中的揪團列表
    """
    groups = Group.get_all()
    return render_template('groups/index.html', groups=groups)

@group_bp.route('/groups/new', methods=['GET'])
def new_group():
    """
    顯示發起揪團的表單
    """
    from app.models.store import Store
    stores = Store.get_all()
    # 獲取所有使用者，以便模擬發起人
    from app.models.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('groups/new.html', stores=stores, users=users)

@group_bp.route('/groups', methods=['POST'])
def create_group():
    """
    接收表單，存入 DB，重導向至大廳
    """
    data = {
        'creator_id': int(request.form.get('creator_id', 1)),
        'store_id': int(request.form.get('store_id', 1)),
        'delivery_fee': int(request.form.get('delivery_fee', 0)),
        'pickup_location': request.form.get('pickup_location'),
        'deadline': request.form.get('deadline'),
        'status': 'open'
    }
    
    if not data['pickup_location'] or not data['deadline']:
        flash("請填寫必填欄位")
        return redirect(url_for('group.new_group'))

    Group.create(data)
    flash("揪團建立成功！")
    return redirect(url_for('group.index'))

@group_bp.route('/groups/<int:id>', methods=['GET'])
def detail(id):
    """
    顯示該團的詳細資訊、所有訂單與結算金額
    """
    group = Group.get_by_id(id)
    if not group:
        return "Group not found", 404
        
    from app.models.store import Store
    store = Store.get_by_id(group['store_id'])
    
    orders = Order.get_by_group_id(id)
    
    # 獲取訂單明細與用戶姓名
    from app.models.order_item import OrderItem
    from app.models.database import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    detailed_orders = []
    for o in orders:
        order_dict = dict(o)
        # 查詢用戶名稱
        cursor.execute("SELECT username FROM users WHERE id = ?", (order_dict['user_id'],))
        u = cursor.fetchone()
        order_dict['username'] = u['username'] if u else f"User {order_dict['user_id']}"
        
        # 查詢訂單細項
        order_dict['items'] = OrderItem.get_by_order_id(order_dict['id'])
        detailed_orders.append(order_dict)
        
    conn.close()
    
    return render_template('groups/detail.html', group=group, store=store, orders=detailed_orders)

@group_bp.route('/groups/<int:id>/close', methods=['POST'])
def close_group(id):
    """
    團長專用：關閉揪團，計算 split_fee 並更新訂單
    """
    group = Group.get_by_id(id)
    if not group:
        return "Group not found", 404
        
    if group['status'] != 'open':
        flash("該揪團已經結單")
        return redirect(url_for('group.detail', id=id))
        
    orders = Order.get_by_group_id(id)
    num_orders = len(orders)
    
    # 執行平攤運費計算
    if num_orders > 0:
        delivery_fee = group['delivery_fee']
        # 使用無條件進位，確保收齊運費
        split_fee = math.ceil(delivery_fee / num_orders)
        
        for order in orders:
            final_amount = order['items_total'] + split_fee
            Order.update(order['id'], {
                'split_fee': split_fee,
                'final_amount': final_amount
            })
            
    # 更新揪團狀態
    Group.update(id, {'status': 'closed'})
    flash("已成功結單並計算好拆帳金額！")
    return redirect(url_for('group.detail', id=id))
