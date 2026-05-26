# empty init file
# This file makes routes a package
from flask import Blueprint

group_bp = Blueprint('group', __name__)
order_bp = Blueprint('order', __name__)

from . import group_routes
from . import order_routes
