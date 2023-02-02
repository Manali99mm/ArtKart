from flask import Blueprint
from controllers.user import get_user

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['GET'])(get_user)