from flask import Blueprint, render_template, request, make_response, session
import mysql.connector

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
    con = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    db = "skillport_db"
    )  
    sql = "INSERT INTO user_tbl (user_name, first_name) VALUES ();"
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