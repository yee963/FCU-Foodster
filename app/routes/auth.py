from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('無效的帳號或密碼')
            return redirect(url_for('auth.login'))
        login_user(user, remember=request.form.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('auth.profile')
        return redirect(next_page)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        
        if user_by_username:
            flash('該帳號（學號）已被註冊。')
            return redirect(url_for('auth.register'))
        if user_by_email:
            flash('該信箱已被註冊。')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('註冊成功！請登入。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        # 檢查信箱是否被其他人使用
        if email != current_user.email:
            user_by_email = User.query.filter_by(email=email).first()
            if user_by_email:
                flash('該信箱已被其他帳號使用。')
                return redirect(url_for('auth.profile'))
                
        current_user.name = name
        current_user.email = email
        db.session.commit()
        flash('個人資料已更新！')
        return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html')

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))
