import os
from flask import Flask
from app.models.database import init_db
from app.routes import group_bp, order_bp

# 建立 Flask 應用程式實例
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-key-for-foodster")

# 初始化資料庫 (若無則自動建立資料表並寫入種子資料)
init_db()

# 註冊 Blueprints
app.register_blueprint(group_bp)
app.register_blueprint(order_bp)

# 首頁路由：轉向至揪團大廳
@app.route('/')
def home():
    from flask import redirect, url_for
    return redirect(url_for('group.index'))

# 導入其他路由 (如店家細節頁面路由)
from app import routes
