from flask import Flask
from app.routes import group_bp, order_bp
import os

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

    # 註冊 Blueprints
    app.register_blueprint(group_bp)
    app.register_blueprint(order_bp)

    @app.route('/')
    def home():
        from flask import redirect, url_for
        return redirect(url_for('group.index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
