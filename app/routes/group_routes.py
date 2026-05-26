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
    # 由於沒有模板，先回傳 JSON 格式以便測試
    return {"groups": groups}, 200

@group_bp.route('/groups/new', methods=['GET'])
def new_group():
    """
    顯示發起揪團的表單
    """
    return "New Group Form Placeholder", 200

@group_bp.route('/groups', methods=['POST'])
def create_group():
    """
    接收表單，存入 DB，重導向至大廳
    """
    data = {
        'creator_id': request.form.get('creator_id', 1), # 預設 user 1 (F-01 尚未整合)
        'store_id': request.form.get('store_id', 1),
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
        
    orders = Order.get_by_group_id(id)
    return {
        "group": group,
        "orders": orders
    }, 200

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
