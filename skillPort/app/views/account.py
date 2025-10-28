from flask import Blueprint, render_template, request, make_response, session

# Blueprintオブジェクトを作成
account_bp = Blueprint('account', __name__, url_prefix='/account')

# /auth/loginにアクセスされた際の処理を記述
@account_bp.route('/register', methods=["GET"])
def register_form():
    
    return render_template('account/register.html')

@account_bp.route('/register_userlogin', methods=["POST"])
def register_userlogin():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template('account/profile.html', username=username, password=password)

@account_bp.route('/register_userinfo', methods=["POST"])
def register_userinfo():
    
    sql = "INSERT INTO user_tbl (user_name, first_name, last_name, first_name_katakana, last_name_katakana, tel_no, zip_code, prefecture, address1, address2, address3, birthday, mail, password, introduction) VALUES ();"
    return render_template('account/profile.html')

@account_bp.route('/profile', methods=["GET"])
def user_profile():
    return render_template('account/profile.html')

@account_bp.route('/my_page_top', methods=["GET"])
def my_page_top():
    return render_template('my_page/mp_top.html')