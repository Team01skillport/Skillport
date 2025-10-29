from flask import Blueprint, render_template, request, make_response, session
from app.db import fetch_query

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/register_userlogin', methods=["GET"])
def register_form():
    
    return render_template('account/account_register.html')

@account_bp.route('/register_userinfo', methods=["POST"])
def register_userlogin():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    return render_template('account/user_register.html', username=username, password=password)

@account_bp.route('/register_success', methods=["POST"])
def register_userinfo():
    username = request.form.get("username")
    password = request.form.get("password")
    mail = request.form.get("email")
    tel_no = request.form.get("tel")
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    last_name_katakana = request.form.get("last_name_katakana")
    first_name_katakana = request.form.get("first_name_katana")
    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    zip_code = request.form.get("zip_code")
    prefecture = request.form.get("prefecture")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    introduction = request.form.get("introduction")
   
    sql = "INSERT INTO user_tbl ('"+username+"', '"+first_name+"', '"+last_name+"', '"+first_name_katakana+"', '"+last_name_katakana+"', '"+tel_no+"', '"+zip_code+"', '"+prefecture+"', '"+address1+"', '"+address2+"', '"+birthday+"', '"+gender+"', '"+mail+"', '"+password+"', '"+introduction+"') VALUES ();"
    # create_user = fetch_query(sql)
    return render_template('account/profile.html')

@account_bp.route('/profile', methods=["GET"])
def user_profile():
    return render_template('account/profile.html')

@account_bp.route('/edit_profile', methods=["GET"])
def edit_profile():
    return render_template('profile/profile_edit.html')

@account_bp.route('/my_page_top', methods=["GET"])
def my_page_top():
    return render_template('my_page/mp_top.html')