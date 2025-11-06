from flask import Blueprint, render_template, request, make_response, session
from app.db import create_user, fetch_query

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



@account_bp.route('/user_register_complete', methods=["POST"])
def user_register_complete():
    username = request.form.get("username")
    password = request.form.get("password")
    mail = request.form.get("email")
    tel_no = request.form.get("tel")
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    last_name_furigana = request.form.get("last_name_furigana")
    first_name_furigana = request.form.get("first_name_furigana")
    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    zip_code = request.form.get("zip_code")
    prefecture = request.form.get("prefecture")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    introduction = request.form.get("introduction")
   
    sql = "INSERT INTO user_tbl (user_name, first_name, last_name, first_name_katakana, last_name_katakana, tel_no, zip_code, prefecture, address1, address2, birthday, gender, mail, password, introduction, profile_icon) VALUES ('"+username+"', '"+first_name+"', '"+last_name+"', '"+first_name_furigana+"', '"+last_name_furigana+"', '"+tel_no+"', '"+zip_code+"', '"+prefecture+"', '"+address1+"', '"+address2+"', '"+birthday+"', '"+gender+"', '"+mail+"', '"+password+"', '"+introduction+"', '/icons/default_icon.png');"
    touroku_dekita = create_user(sql)
    print(touroku_dekita)
    return render_template('account/user_register_success.html')

@account_bp.route('/edit_profile/<user_name>', methods=["GET"])
def edit_profile(user_name):
    sql = "SELECT * FROM user_tbl WHERE user_name = '"+str(user_name)+"';"
    user_info = fetch_query(sql, params=None, fetch_one=True)
    return render_template('profile/profile_edit.html', info=user_info, user_name=user_name)

@account_bp.route('/edit_profile/<user_name>/success', methods=["POST"])
def edit_profile_success(user_name):

    mail = request.form.get("email")
    tel_no = request.form.get("tel")
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    last_name_furigana = request.form.get("last_name_furigana")
    first_name_furigana = request.form.get("first_name_furigana")
    birthday = request.form.get("birthday")
    zip_code = request.form.get("zip_code")
    prefecture = request.form.get("prefecture")
    address1 = request.form.get("address1")
    address2 = request.form.get("address2")
    new_profile_icon = request.form.get("profile_icon")
    introduction = request.form.get("introduction")
    
    sql = "INSERT INTO user_tbl (user_name, first_name, last_name, first_name_katakana, last_name_katakana, tel_no, zip_code, prefecture, address1, address2, birthday, gender, mail, password, introduction, profile_icon) VALUES ('"+username+"', '"+first_name+"', '"+last_name+"', '"+first_name_furigana+"', '"+last_name_furigana+"', '"+tel_no+"', '"+zip_code+"', '"+prefecture+"', '"+address1+"', '"+address2+"', '"+birthday+"', '"+gender+"', '"+mail+"', '"+password+"', '"+introduction+"', '"+new_profile_icon+"');"
    update_user_info = create_user(sql)
    print(update_user_info)

    sql = "SELECT * FROM user_tbl WHERE user_name = '"+str(user_name)+"';"
    user_info = fetch_query(sql, params=None, fetch_one=True)
    return render_template('profile/profile_edit.html')

@account_bp.route('/my_page_top', methods=["GET"])
def my_page_top():
    return render_template('my_page/mp_top.html')