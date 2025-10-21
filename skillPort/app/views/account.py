from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
account_bp = Blueprint('account', __name__, url_prefix='/account')

# /auth/loginにアクセスされた際の処理を記述
@account_bp.route('/account/register', methods=["GET"])
def register_form():
    
    return render_template('account/register.html')

@account_bp.route('/account/profile', methods=["GET"])
def user_profile():
    return render_template('account/profile.html')