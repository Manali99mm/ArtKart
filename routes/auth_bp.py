from flask import Blueprint
from controllers.auth import register, login, verifyOTP, validateOTP

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/verifyotp', methods=['POST'])(verifyOTP)
auth_bp.route('/validateotp', methods=['POST'])(validateOTP)