from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-for-foodster'

from app import routes
