from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# /auth/loginにアクセスされた際の処理を記述
@auth_bp.route('/auth/login', methods=["GET"])
def login_form():
    errtbl = {}
    user_id = "guest"
    return render_template('auth/login.html', user_id=user_id, errtbl=errtbl)
